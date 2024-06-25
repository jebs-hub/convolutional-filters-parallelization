import re
import os
import argparse
import matplotlib.pyplot as plt

# Function to extract metrics from a perf stat output file
def extract_metrics(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    metrics = {}
    
    # Extract cycles
    match = re.search(r'(\d{1,3}(?:\.\d{3})+)      cpu_core/cycles/', content)
    if not match:
        match = re.search(r'(\d{1,3}(?:\.\d{3})+)      cycles', content)
    if not match:
        match = re.search(r'(\d[\d,]*)\s+cpu_core/cycles/u', content)
    if match:
        metrics['cycles'] = int(match.group(1).replace('.', '').replace(',', ''))
    else:
        metrics['cycles'] = None

    # Extract instructions
    match = re.search(r'(\d{1,3}(?:\.\d{3})+)      cpu_core/instructions/', content)
    if not match:
        match = re.search(r'(\d{1,3}(?:\.\d{3})+)      instructions', content)
    if not match:
        match = re.search(r'(\d[\d,]*)\s+cpu_core/instructions/u', content)
    
    if match:
        metrics['instructions'] = int(match.group(1).replace('.', '').replace(',', ''))
    else:
        metrics['instructions'] = None

    # Extract elapsed time
    match = re.search(r'(\d{1,2},\d{9}) seconds time elapsed', content)
    if not match:
        match = re.search(r'(\d+\.\d+) seconds time elapsed', content)
    if match:
        metrics['time_elapsed'] = float(match.group(1).replace(',', '.'))
    else:
        metrics['time_elapsed'] = None

    # Extract elapsed time
    match = re.search(r'(\d+\.\d+)\s+CPUs utilized', content)
    if match:
        metrics['cpus_utilized'] = float(match.group(1).replace(',', '.'))
    else:
        metrics['cpus_utilized'] = None

    # Extract elapsed time
    metrics['task_clock'] = float(content.strip().split('\n')[5].split()[0])
    
    return metrics


# Function to plot the metrics
def plot_metrics(metrics):
    threads = sorted(metrics.keys())

    cycles = [metrics[t]['cycles'] for t in threads]
    instructions = [metrics[t]['instructions'] for t in threads]
    time_elapsed = [metrics[t]['time_elapsed'] for t in threads]
    cpus_utilized = [metrics[t]['cpus_utilized'] for t in threads]
    task_clock = [metrics[t]['task_clock'] for t in threads]

    print("times: ",time_elapsed)
    print("cycles: ",cycles)
    print("instructions: ",instructions)
    print("CPUs utilized: ",cpus_utilized)
    plt.figure(figsize=(15, 5))

    # plt.subplot(1, 3, 1)
    # plt.plot(threads, cycles, marker='o')
    # plt.xlabel('Number of Threads')
    # plt.ylabel('Cycles')
    # plt.title('CPU Core Cycles vs Number of Threads')
    plt.subplot(1, 3, 1)
    plt.plot(threads, task_clock, marker='o')
    plt.xlabel('Number of Threads')
    plt.ylabel('Task Clock')
    plt.title('CPU Task Clock vs Number of Threads')

    # plt.subplot(1, 3, 2)
    # plt.plot(threads, instructions, marker='o')
    # plt.xlabel('Number of Threads')
    # plt.ylabel('Instructions')
    # plt.title('CPU Core Instructions vs Number of Threads')

    plt.subplot(1, 3, 3)
    plt.plot(threads, time_elapsed, marker='o')
    plt.xlabel('Number of Threads')
    plt.ylabel('Time Elapsed (seconds)')
    plt.title('Time Elapsed vs Number of Threads')

    plt.subplot(1, 3, 2)
    plt.plot(threads, cpus_utilized, marker='o')
    plt.xlabel('Number of Threads')
    plt.ylabel('CPUs Utilized')
    plt.title('CPUs Utilized vs Number of Threads')

    plt.tight_layout()
    plt.show()

# Main function
def main():
    parser = argparse.ArgumentParser(description="A script to demonstrate command-line arguments with a 'program' argument.")
    parser.add_argument("program", type=str, help="The name of the program.")
    args = parser.parse_args()
    perf_output_dir = 'perf_outputs'
    metrics = {}
    files = os.listdir(perf_output_dir)
    
    valid_files = [filename for filename in files if args.program in filename and 'm' not in filename]
    for filename in valid_files:
        i = int(re.search(r'_(\d+)\.txt$', filename).group(1))
        metrics[i] = extract_metrics(perf_output_dir+'/'+filename)
    plot_metrics(metrics)

if __name__ == '__main__':
    main()
