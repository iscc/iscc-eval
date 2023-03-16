# -*- coding: utf-8 -*-
"""Create Transcoded Variations of audio files"""
import os
from os.path import splitext, basename, abspath, join
from subprocess import run
import iscc_eval as ie
from loguru import logger as log
from pathlib import Path
from humanize import naturalsize
from iscc_sdk.tools import ffmpeg_bin


target_formats = (
    # 'ac3_64000',
    # 'aac_64000',
    "aif_64000",
    #'mp2_64000',
    # 'mp3_64000',
    "opus_64000",
    "wv_64000",
)


def create_file_variations(fp, outpath):
    """Builds/Caches/Returns a list of encoding variations for a given audio file"""
    in_name, in_ext = splitext(basename(fp))
    variations = []
    for tf in target_formats:
        fmt, bitrate = tf.split("_")
        out_path = abspath(join(outpath, f"v_{in_name}-{bitrate}.{fmt}"))
        # generate if it does not exist:
        if not os.path.exists(out_path):
            run([ffmpeg_bin(), "-i", fp, "-b:a", bitrate, out_path], check=True)
        variations.append(out_path)
    return variations


def create_dir_variations(src: Path, dst: Path) -> None:
    total, files = ie.get_files(src, mode="audio")
    log.debug(
        f"Creating variatons for {len(files)} audio files with total size of {naturalsize(total)}"
    )
    variations = []
    for file in files:
        v = create_file_variations(file, dst)
        variations.extend(v)
    return variations


def sample():
    import shutil

    n_clusters = 100
    cluster_dir = ie.cnf.data_dir / "clusters"
    cluster_dir.mkdir(parents=True, exist_ok=True)

    for idx, fp in enumerate(ie.fma_small()):
        if idx > n_clusters:
            shutil.copy(fp, cluster_dir)
            continue
        fp = Path(fp)
        # Create dir for file cluster
        file_cluster_dir = cluster_dir / fp.stem
        file_cluster_dir.mkdir(parents=True, exist_ok=True)
        # Copy source file to clusterdir
        shutil.copy(fp, file_cluster_dir)
        # Create variations
        create_file_variations(fp, file_cluster_dir)


if __name__ == "__main__":
    sample()
