import re
import os
import matplotlib.pyplot as plt

# Function to extract metrics from a perf stat output file
def extract_metrics(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    metrics = {}
    
    # Extract cycles
    match = re.search(r'(\d{1,3}(?:\.\d{3})+)      cpu_core/cycles/', content)
    if match:
        metrics['cycles'] = int(match.group(1).replace('.', ''))
    else:
        metrics['cycles'] = None

    # Extract instructions
    match = re.search(r'(\d{1,3}(?:\.\d{3})+)      cpu_core/instructions/', content)
    if match:
        metrics['instructions'] = int(match.group(1).replace('.', ''))
    else:
        metrics['instructions'] = None

    # Extract elapsed time
    match = re.search(r'(\d{1,2},\d{9}) seconds time elapsed', content)
    if match:
        metrics['time_elapsed'] = float(match.group(1).replace(',', ''))
    else:
        metrics['time_elapsed'] = None
    
    return metrics


# Function to plot the metrics
def plot_metrics(metrics):
    threads = sorted(metrics.keys())

    cycles = [metrics[t]['cycles'] for t in threads]
    instructions = [metrics[t]['instructions'] for t in threads]
    time_elapsed = [metrics[t]['time_elapsed'] for t in threads]
    print("times: ",time_elapsed)
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.plot(threads, cycles, marker='o')
    plt.xlabel('Number of Threads')
    plt.ylabel('Cycles')
    plt.title('CPU Core Cycles vs Number of Threads')

    plt.subplot(1, 3, 2)
    plt.plot(threads, instructions, marker='o')
    plt.xlabel('Number of Threads')
    plt.ylabel('Instructions')
    plt.title('CPU Core Instructions vs Number of Threads')

    plt.subplot(1, 3, 3)
    plt.plot(threads, time_elapsed, marker='o')
    plt.xlabel('Number of Threads')
    plt.ylabel('Time Elapsed (seconds)')
    plt.title('Time Elapsed vs Number of Threads')

    plt.tight_layout()
    plt.show()

# Main function
def main():
    perf_output_dir = 'perf_outputs'
    metrics = {}
    files = os.listdir(perf_output_dir)
    i = 1
    for filename in files:
        metrics[i] = extract_metrics(perf_output_dir+'/'+filename)
        i +=1
    plot_metrics(metrics)

if __name__ == '__main__':
    main()