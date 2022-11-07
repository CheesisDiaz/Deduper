#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --cpus-per-task=4
#SBATCH --partition=bgmp
#SBATCH --nodes=1
#SBATCH --time=0-10:00:00
#SBATCH --job-name=deduping

conda activate bgmp_py310

# /usr/bin/time -v ./Deduper.py \
#     -f "test/unit_test.sam" \
#     -o "test/unit_test_result.sam" \
#     -u "STL96.txt"

/usr/bin/time -v ./diaz_deduper.py \
    -f C1_SE_uniqAlignSort.sam \
    -o C1_SE_uniqAlign_Deduped.sam \
    -u STL96.txt


