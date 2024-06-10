#!/bin/bash

#TODO separate Makefile for this
gcc conv_filter_serial.c -o conv_filter_serial

image_directory="images/ppms"

rm "images/ppms/out/*"

if [ ! -d "$image_directory" ]; then
  echo "Directory $image_directory does not exist."
  exit 1
fi


for input_image in $image_directory/*.ppm; do
  filename=$(basename "$input_image")
  c_output_image="images/ppms/out/${filename%.ppm}_c_output.ppm"
  python_output_image="images/ppms/out/${filename%.ppm}_python_output.ppm"

  echo "images/ppms/out/${filename%.ppm}_c_output.ppm"

  start_c=$(date +%s%N)
  ./conv_filter_serial $input_image $c_output_image
  end_c=$(date +%s%N)

  elapsed_c=$((($end_c - $start_c)/1000000))

  start_python=$(date +%s%N)
  python3 conv_filter_serial.py $input_image $python_output_image
  end_python=$(date +%s%N)

  elapsed_python=$((($end_python - $start_python)/1000000))

  echo "Processing $input_image:"
  echo "  Execution time for C program: $elapsed_c ms"
  echo "  Execution time for Python program: $elapsed_python ms"
  echo
done
