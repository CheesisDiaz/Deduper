#!/bin/bash
#SBATCH --account=bgmp
#SBATCH --cpus-per-task=4
#SBATCH --partition=bgmp
#SBATCH --nodes=1
#SBATCH --time=0-10:00:00
#SBATCH --job-name=deduping

conda activate bgmp_py310

samtools sort /projects/bgmp/shared/deduper/C1_SE_uniqAlign.sam -o C1_SE_uniqAlignSort.sam

# /usr/bin/time -v ./Deduper.py \
#     -f "test/test_file.sam" \
#     -o "test/test_fileout.sam" \
#     -u "test/umi_test.txt"

/usr/bin/time -v ./Deduper.py \
    -f "C1_SE_uniqAlignSort.sam" \
    -o "C1_SE_uniqAlign_Deduped_clean.sam" \
    -u "STL96.txt"