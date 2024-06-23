cmake_minimum_required(VERSION 3.9)

project(prime)

find_package(OpenMP REQUIRED)

set(CMAKE_C_STANDARD 99)

add_executable(serial   conv_filter_serial.c)
add_executable(parallel conv_filter.c)
add_executable(for_parallel conv_filter_for.c)
target_link_libraries(serial
    PUBLIC OpenMP::OpenMP_C)

target_link_libraries(parallel
    PUBLIC OpenMP::OpenMP_C)
target_link_libraries(for_parallel
    PUBLIC OpenMP::OpenMP_C)