import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Configuration ---
# The script expects the 'results.csv' file to be in a subfolder of the current directory.
# For example, if you run from 'pda-otsu-cuda-openmp', it will look in 'pda-otsu-cuda-openmp/imagini_test/output/results.csv'
# You might need to adjust this path depending on your folder structure.
CSV_FILE_PATH = 'imagini_test/output/results.csv'
OUTPUT_DIR = 'plotting'

# --- Main Script ---
def main():
    if not os.path.exists(CSV_FILE_PATH):
        print(f"Error: CSV file not found at '{CSV_FILE_PATH}'")
        print("Please run the C++ project first to generate the results.csv file.")
        return

    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Read the data
    df = pd.read_csv(CSV_FILE_PATH)

    # Sort by number of pixels for a clean plot
    df = df.sort_values(by='Pixels')

    # --- 1. Execution Time vs. Image Size ---
    plt.figure(figsize=(12, 8))
    plt.plot(df['Pixels'], df['Time_CPU_ms'], marker='o', linestyle='-', label='CPU (Sequential)')
    plt.plot(df['Pixels'], df['Time_OMP_ms'], marker='s', linestyle='-', label='OpenMP')
    plt.plot(df['Pixels'], df['Time_CUDA_ms'], marker='^', linestyle='-', label='CUDA')

    plt.xscale('log')
    plt.yscale('log')
    plt.title('Execution Time vs. Image Size (Log-Log Scale)')
    plt.xlabel('Image Size (Total Pixels)')
    plt.ylabel('Execution Time (milliseconds)')
    plt.grid(True, which="both", ls="--")
    plt.legend()

    time_plot_path = os.path.join(OUTPUT_DIR, 'execution_time_vs_size.png')
    plt.savefig(time_plot_path)
    print(f"Saved time plot to '{time_plot_path}'")
    plt.close()


    # --- 2. Speedup vs. Image Size ---
    # Speedup is calculated as T_cpu / T_parallel
    df['Speedup_OMP'] = df['Time_CPU_ms'] / df['Time_OMP_ms']
    df['Speedup_CUDA'] = df['Time_CPU_ms'] / df['Time_CUDA_ms']

    plt.figure(figsize=(12, 8))
    plt.plot(df['Pixels'], df['Speedup_OMP'], marker='s', linestyle='-', label='Speedup OpenMP vs. CPU')
    plt.plot(df['Pixels'], df['Speedup_CUDA'], marker='^', linestyle='-', label='Speedup CUDA vs. CPU')

    plt.xscale('log')
    plt.title('Speedup vs. Image Size')
    plt.xlabel('Image Size (Total Pixels)')
    plt.ylabel('Speedup (Factor, e.g., 2x, 10x)')
    plt.grid(True, which="both", ls="--")
    plt.legend()
    # Add a horizontal line at y=1 for reference (no speedup)
    plt.axhline(y=1, color='r', linestyle='--', label='No Speedup')

    speedup_plot_path = os.path.join(OUTPUT_DIR, 'speedup_vs_size.png')
    plt.savefig(speedup_plot_path)
    print(f"Saved speedup plot to '{speedup_plot_path}'")
    plt.close()

if __name__ == '__main__':
    main()
