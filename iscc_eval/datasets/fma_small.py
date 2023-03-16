# -*- coding: utf-8 -*-
"""Read audio data from Free Music Archive (FMA).

Records: 8000 tracks of 30s
Size: 7.2 GiB (compressed) - 7.44 GB uncompressed
Info: https://github.com/mdeff/fma
Data: https://os.unil.cloud.switch.ch/fma/fma_small.zip

Instructions:
    First iteration over fma_small will download and extract audio files.
"""
import os
from loguru import logger as log
import zipfile
import iscc_eval as ie
from blake3 import blake3


__all__ = ["fma_small"]

DOWNLOAD_URL = "https://os.unil.cloud.switch.ch/fma/fma_small.zip"
DATA_PATH = os.path.join(ie.cnf.data_dir, "fma_small")
DATA_FILE_PATH = os.path.join(DATA_PATH, "fma_small.zip")


def fma_small():
    """Yield file path to all audio tracks from fma_small dataset."""
    try:
        os.makedirs(DATA_PATH)
        log.info("Created data directory: {}".format(DATA_PATH))
    except FileExistsError:
        pass

    if not os.path.exists(DATA_FILE_PATH):
        log.info("Downloading fma_small data: {}".format(DATA_FILE_PATH))
        ie.download(DOWNLOAD_URL, DATA_FILE_PATH)

        log.info("Unpacking audio tracks: {}".format(DATA_FILE_PATH))
        with zipfile.ZipFile(DATA_FILE_PATH) as zf:
            zf.extractall(DATA_PATH)

    for fp in ie.iter_files(DATA_PATH, exts=["mp3"], recursive=True):
        yield fp


if __name__ == "__main__":
    sigs = {}
    log.info("check fma_small for exact duplicate tracks")
    for image_path in fma_small():
        sig = blake3(open(image_path, "rb").read()).hexdigest()
        if sig not in sigs:
            sigs[sig] = image_path
        else:
            print("Collision: {} -> {}".format(image_path, sigs[sig]))
    log.info("done checking fma_small for exact duplicate tracks")
