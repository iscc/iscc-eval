from statistics import mean
from typing import List, Tuple
import typer
import iscc_core as ic
import iscc_sdk as idk
from diskcache import Index
import iscc_eval as ie
from pathlib import Path
from rich import print
from rich.progress import track
from iscc_eval import state


app = typer.Typer(no_args_is_help=True, help="ISCC matching accuracy benchmarks")


def query(db: Index, iscc: bytes, th: int = 10) -> List[str]:
    """Match `iscc` against `db` items with threshold `th`"""
    matches = []
    for cluster in db.values():
        for item in cluster:
            dist = ic.iscc_distance_bytes(iscc, item)
            if dist <= th:
                matches.append(item)
    return matches


def evaluate(gdb: Index, mdb: dict) -> Tuple[float, float, float]:
    """Calculate recall, precision and F1 score for matches (mdb) against ground truth (gdb)"""
    precisions = []
    recall = []
    f1_score = []
    for k, relevant in track(gdb.items(), description="Evaluating..."):
        if k == "samples":
            continue
        rel = set(relevant)
        ret = set(mdb[k])
        if len(rel) == 0 and len(ret) == 0:
            precisions.append(1.0)
            recall.append(1.0)
            continue
        try:
            prec = len(rel.intersection(ret)) / len(ret)
        except ZeroDivisionError:
            prec = 0
        precisions.append(prec)
        rec = len(rel.intersection(ret)) / len(rel)
        recall.append(rec)
        try:
            f1 = 2 * ((prec * rec) / (prec + rec))
        except ZeroDivisionError:
            f1 = 0
        f1_score.append(f1)
        if state["verbose"]:
            print(f"Query {k.hex()} -> Recall {rec:.2f} - Precision {prec:.2f} - F1 {f1:.2f}")
    return mean(recall), mean(precisions), mean(f1_score)


def db_info(db):
    queries = len(db) - 1
    samples = 0
    for value in db.values():
        samples += len(value)
    print(f"Dataset has {queries} queries against {samples} samples\n")


def ground_truth(path: Path, bits: int):
    """Generate or load cached ground truth data for cluster path"""
    db_path: Path = ie.cnf.data_dir / f"{ie.dirhash(path)[:16]}_{bits}"
    if db_path.exists():
        # Load existing ground truth data
        print(f"\nUsing cached ground truth for {path} from {db_path}")
        gdb = Index(db_path.as_posix())
        db_info(gdb)
        return gdb
    else:
        # Build ground truth data
        print(f"\nProcessing ground truth for {path} to db {db_path}")
        db_path.mkdir(parents=True, exist_ok=False)
        gdb = Index(db_path.as_posix())
        gdb["samples"] = []
        for item in track(sorted(path.iterdir()), description="Processing..."):
            if item.is_dir():
                cluster_key = item.name
                total, files = ie.get_files(item)
                qkey = None
                result = []
                for idx, fp in enumerate(sorted(files)):
                    try:
                        iscc_meta = idk.code_content(fp.as_posix())
                    except Exception as e:
                        if state["verbose"]:
                            print(f"Failed code generation for {item} with {e}")
                        continue
                    result.append(iscc_meta.iscc)
                    iscc_bytes = iscc_meta.iscc_obj.hash_bytes
                    if idx == 0:
                        # First file in cluster is the query instance
                        qkey = iscc_bytes
                        gdb[qkey] = []
                        continue
                    gdb[qkey] = gdb[qkey] + [iscc_bytes]
                if state["verbose"]:
                    print(f"Cluster {cluster_key} ground truth: {result[0]} -> {result[1:]}")
                cluster_distances = []
                for target in gdb[qkey]:
                    cluster_distances.append(ic.iscc_distance_bytes(qkey, target))
                if state["verbose"]:
                    print(f"Cluster {cluster_key} distances: {cluster_distances}")
            elif item.is_file():
                try:
                    iscc_meta = idk.code_content(item.as_posix())
                    if state["verbose"]:
                        print(f"Sample {iscc_meta.iscc} <- {item.name}")
                except Exception as e:
                    if state["verbose"]:
                        print(f"Failed code generation for {item} with {e}")
                    continue

                iscc_bytes = iscc_meta.iscc_obj.hash_bytes
                gdb["samples"] = gdb["samples"] + [iscc_bytes]

        db_info(gdb)
        return gdb


@app.command()
def content_code(
    path: Path = typer.Argument(..., help="Path to folder with test files"),
    th: int = typer.Option(8, help="Threshold for matching (bit difference)."),
    bits: int = typer.Option(64, help="Content-Code length in number of bits (64, 128, 256)"),
):
    idk.sdk_opts.extract_metadata = False
    ic.core_opts.audio_bits = bits
    assert bits in (64, 128, 256)

    # Detect Perceptual mode
    mode = None
    for item in path.rglob("*"):
        if item.is_file():
            mtype, mode = idk.mediatype_and_mode(item.as_posix())
            mode = mode.title()
            if state["verbose"]:
                print(f"\nAssuming perceptual mode {mode} based on {item.name}")
            break

    code_type = f"{mode}-Code"
    print(f"\n[bold]ISCC Matching Benchmark - {code_type} {bits}-bits - Threshold {th}[/bold]")
    print("==========================================================================\n")
    gdb = ground_truth(path, bits)
    mdb = dict()  # Matches DB
    print(f"Matching {bits}-bit {code_type}s with threshold {th}-bit distance")
    for item in track(gdb.keys(), description="Matching..."):
        if item != "samples":
            mdb[item] = query(gdb, item, th)
    print(f"\nEvaluating matches with {th}-bit distance")
    recall, prec, f1 = evaluate(gdb, mdb)
    print(
        f"\n[bold yellow on red]Matching result: Recall {recall:.2f} - Precision {prec:.2f} - F1 {f1:.2f} (with {th}-bit threshold)\n"
    )


if __name__ == "__main__":
    app()
