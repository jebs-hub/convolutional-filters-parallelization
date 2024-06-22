cmake_minimum_required(VERSION 3.9)

project(prime)

find_package(OpenMP REQUIRED)

set(CMAKE_C_STANDARD 99)

add_executable(serial   conv_filter_serial.c)
add_executable(parallel_for conv_filter_for.c)
add_executable(parallel_task conv_filter_task.c)

target_link_libraries(serial
    PUBLIC OpenMP::OpenMP_C)

target_link_libraries(parallel_for
    PUBLIC OpenMP::OpenMP_C)

target_link_libraries(parallel_task
    PUBLIC OpenMP::OpenMP_C)
