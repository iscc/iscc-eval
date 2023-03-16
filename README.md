# ISCC Performance Evaluation

## Development Requirements:

- [Python](https://www.python.org/)  3.11
- [Poetry](https://pypi.org/project/poetry/)

## Development Installation:

```shell
$ git clone https://github.com/iscc/iscc-eval.git
$ cd iscc-eval
$ poetry install
```

## Usage:

### Show command line help

```shell
$ iscc-eval --help
```

### Evaluate Content-Code matching accuracy

The `match` command will evaluate **Recall**, **Precision** and **F1 Score** for a given dataset
where:

- `Recall` - how many relevant items are retrieved
- `Precision` - how many retrieved items are relevant
- `F1 Score` - harmonic mean of precision and recall

For a more detailed explanation of the metrics see:
https://en.wikipedia.org/wiki/Precision_and_recall

To evaluate Content-Code matching accuracy you need to prepare ground truth data as follows:

- Create an empty folder for your evaluation data (for example `mydata`)
- Put all your unique media assets into `mydata` (no duplicates or near-duplicates).
- Make sure all media assets are of the same perceptual mode (text, image, audio or video)
- Create ground truth data by:
  - Take a single asset from `mydata` and **move** it into a subdirectory (for example `cluster1`)
  - In the subdirectory create 0 or more variations of the media asset that should be matched
  - Repeat for as many of the assets from the top-level directory as you like

#### Evaluation data directory structure

    mydata
    ├── cluster1                # Subfolders are collections of media assets that should match
    │   ├── 0_original.mp3      # The first file will be the query file (lexicographic sorting)
    │   ├── variation_1.mp3     # A modified version that should match against the query file
    │   └── ...                 # Create as many modified versions as you like
    ├── cluster_x               # A cluster folder can have any name
    │   ├── file1.mp3           # Files in cluster folders can have any name
    │   └── ...                 # A cluster folder may have only one file (query with no match)
    ├── sample1.mp3             # Top-Level files that should NOT match against any of the queries
    ├── sample2.mp3
    └── ...

The `match` command will generate Content-Codes for all media assets in `mydata` recursively and
create ground truth data (expected results) from the `cluster` subfolders.
The first file from each `cluster`-folder will be queried against all other (non-query) files of
the dataset. The query results are then compared against the expected results (ground truth).

Evaluate the matching accuracy with the following command:

```shell
iscc-eval match content-code /path/to/mydata
```

To enable verbose output and a custom Code-Length and matching threshold use:

```shell
iscc-eval --verbose match content-code /path/to/mydata --bits=256 --th=15
```

Sample verbose command output:

```shell
$ iscc-eval --verbose match content-code ./audio-match-sample-data
Will produce verbose output

Assuming perceptual mode Audio based on 154303.mp3

ISCC Matching Benchmark - Audio-Code 64-bits - Threshold 8
==========================================================================

Calculating directory hash for 28 files in ./audio-match-sample-data
Verifying... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

Processing ground truth for ./audio-match-sample-data to db e:\iscc-eval\195d2dc646994ec4_64
Cluster 000002 ground truth: ISCC:EIA5SXHVP7MV55JO -> ['ISCC:EIA5SXHVP7MV55JO', 'ISCC:EIA5SVPVP7NV55JO', 'ISCC:EIA5SXHVP7MV55JO']
Cluster 000002 distances: [0, 3, 0]
Cluster 000005 ground truth: ISCC:EIAVMHXBM5LH6YPH -> ['ISCC:EIAVMHXBM5LH6YPH', 'ISCC:EIAVMPXBM5KF4YPH', 'ISCC:EIAVMHXBM5LH6YPH']
Cluster 000005 distances: [0, 4, 0]
Cluster 000010 ground truth: ISCC:EIA4C6PVOLCXRNHG -> ['ISCC:EIA4C6PVOLCXRNHG', 'ISCC:EIA4C6PVOLCXRNDG', 'ISCC:EIA4C6PVOLCXRNHG']
Cluster 000010 distances: [0, 1, 0]
Cluster 000140 ground truth: ISCC:EIAWEDFYF2RC5OFO -> ['ISCC:EIAWEDFYF2RC5OFO', 'ISCC:EIAWADFYF2RC5OFO', 'ISCC:EIAWEDFYF2RC5OFO']
Cluster 000140 distances: [0, 1, 0]
Cluster 000141 ground truth: ISCC:EIASFKFYBYIKZARK -> ['ISCC:EIASFKFYBYIKZARK', 'ISCC:EIASFKFYBYIKZARK', 'ISCC:EIASFKFYBYIKZARK']
Cluster 000141 distances: [0, 0, 0]
Sample ISCC:EIAYK5R5IOCXNLOD <- 154303.mp3
Sample ISCC:EIAYSZFZGYAWYOJV <- 154305.mp3
Sample ISCC:EIARARPNGMIG7DDT <- 154306.mp3
Sample ISCC:EIAXKYHZF2UPU2GC <- 154307.mp3
Sample ISCC:EIA426FVPZCUYJL6 <- 154308.mp3
Sample ISCC:EIA2JNJVW3K3INNW <- 154309.mp3
Sample ISCC:EIAQQQPZOYDDBKAC <- 154413.mp3
Sample ISCC:EIA64AFJUTUCRCHE <- 154414.mp3
Processing... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
Dataset has 5 queries against 23 samples

Matching 64-bit Audio-Codes with threshold 8-bit distance
Matching... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

Evaluating matches with 8-bit distance
Query d95cf57fd95ef52e -> Recall 1.00 - Precision 1.00 - F1 1.00
Query 561ee167567f61e7 -> Recall 1.00 - Precision 1.00 - F1 1.00
Query c179f572c578b4e6 -> Recall 1.00 - Precision 1.00 - F1 1.00
Query 620cb82ea22eb8ae -> Recall 1.00 - Precision 1.00 - F1 1.00
Query 22a8b80e10ac822a -> Recall 1.00 - Precision 1.00 - F1 1.00
Evaluating... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00

Matching result: Recall 1.00 - Precision 1.00 - F1 1.00 (with 8-bit threshold)

```



### Processing speed evaluation

Run speed benchmark with your own files:

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

