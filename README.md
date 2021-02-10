# ISCC Performance Evaluation

## Requirements:

- [Python](https://www.python.org/) > 3.6
- [Poetry](https://pypi.org/project/poetry/)

## Installation:

```shell
$ git clone https://github.com/iscc/iscc-eval.git
$ cd iscc-eval
$ poetry install
```

## Usage:

```shell
$ iscc-eval --help
Usage: iscc-eval [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  data-code      Benchmark Data-Code processing speed.
  instance-code  Benchmark Instance-Code processing speed.
```

Run a benchmark with your own files:

```shell
$ iscc-eval instance-code /my-asstes-folder

ISCC Performance Benchmark - Instance-Code
==========================================================================
CPU:     Intel(R) Core(TM) i7-7700K CPU @ 4.20GHz
Cores:   8
OS:      Windows-10-10.0.19041-SP0
Python:  CPython - 3.8.0 - MSC v.1916 64 bit (AMD64)
ISCC:    1.1.0-alpha.1
==========================================================================

Benchmarking with 420 files (total size: 11.2 GB).
Result: 2.6 GB/second (with 420 files)
```

