#!/bin/bash

# Usage: ./run_perf.sh <input_image> <output_image_prefix> <program>
echo $"$#"
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <input_image> <output_image_prefix> <program>"
    exit 1
fi

INPUT_IMAGE=$1
OUTPUT_PREFIX=$2
PROGRAM=$3

# Create a directory to store the perf stat outputs
mkdir -p perf_outputs

for THREADS in {1..12}; do
    OUTPUT_IMAGE="${OUTPUT_PREFIX}_${THREADS}.ppm"
    PERF_OUTPUT="perf_outputs/perf_stat_${THREADS}.txt"
    
    echo "Running with ${THREADS} threads..."
    perf stat -o ${PERF_OUTPUT} ./${PROGRAM} ${INPUT_IMAGE} ${OUTPUT_IMAGE} ${THREADS}
    echo "stat -o ${PERF_OUTPUT} ./${PROGRAM} ${INPUT_IMAGE} ${OUTPUT_IMAGE} ${THREADS}"
done

echo "All runs completed. Perf stat outputs are saved in the 'perf_outputs' directory."
