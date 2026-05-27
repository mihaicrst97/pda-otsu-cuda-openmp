import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# --- Configuration ---
# Get the absolute path to the directory containing this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# The project root is one level up from the 'plotting' directory
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Construct absolute paths
CSV_FILE_PATH = os.path.join(PROJECT_ROOT, 'images', 'output', 'results.csv')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'plotting')

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

    # --- Calculate Speedup and Efficiency ---
    # Speedup = T_cpu / T_parallel
    df['Speedup_OMP'] = df['Time_CPU_ms'] / df['Time_OMP_ms']
    df['Speedup_TBB'] = df['Time_CPU_ms'] / df['Time_TBB_ms']

    # Efficiency = Speedup / Number of Threads
    df['Efficiency_OMP'] = df['Speedup_OMP'] / df['Threads_OMP']
    df['Efficiency_TBB'] = df['Speedup_TBB'] / df['Threads_TBB']

    # --- Calculate Average Metrics ---
    # We calculate the average across all images processed in the CSV
    avg_metrics = {
        'Time_CPU': df['Time_CPU_ms'].mean(),
        'Time_OMP': df['Time_OMP_ms'].mean(),
        'Time_TBB': df['Time_TBB_ms'].mean(),
        'Speedup_OMP': df['Speedup_OMP'].mean(),
        'Speedup_TBB': df['Speedup_TBB'].mean(),
        'Efficiency_OMP': df['Efficiency_OMP'].mean(),
        'Efficiency_TBB': df['Efficiency_TBB'].mean(),
    }

    print("Average Metrics:")
    for key, value in avg_metrics.items():
        print(f"  {key}: {value:.4f}")

    # --- 1. Execution Time Comparison ---
    plt.figure(figsize=(10, 6))
    methods = ['CPU', 'OpenMP', 'TBB']
    times = [avg_metrics['Time_CPU'], avg_metrics['Time_OMP'], avg_metrics['Time_TBB']]
    
    bars = plt.bar(methods, times, color=['skyblue', 'lightgreen', 'salmon'])
    plt.ylabel('Average Execution Time (ms)')
    plt.title('Average Execution Time Comparison')
    plt.bar_label(bars, fmt='%.2f ms')

    time_plot_path = os.path.join(OUTPUT_DIR, 'time_comparison.png')
    plt.savefig(time_plot_path)
    print(f"\nSaved time comparison plot to '{time_plot_path}'")
    plt.close()

    # --- 2. Speedup Comparison ---
    plt.figure(figsize=(10, 6))
    parallel_methods = ['OpenMP', 'TBB']
    speedups = [avg_metrics['Speedup_OMP'], avg_metrics['Speedup_TBB']]

    bars = plt.bar(parallel_methods, speedups, color=['lightgreen', 'salmon'])
    plt.axhline(y=1, color='r', linestyle='--', label='No Speedup')
    plt.ylabel('Speedup Factor (vs. CPU)')
    plt.title('Average Speedup Comparison')
    plt.bar_label(bars, fmt='%.2fx')
    
    speedup_plot_path = os.path.join(OUTPUT_DIR, 'speedup_comparison.png')
    plt.savefig(speedup_plot_path)
    print(f"Saved speedup comparison plot to '{speedup_plot_path}'")
    plt.close()

    # --- 3. Efficiency Comparison ---
    plt.figure(figsize=(10, 6))
    efficiencies = [avg_metrics['Efficiency_OMP'], avg_metrics['Efficiency_TBB']]

    bars = plt.bar(parallel_methods, efficiencies, color=['lightgreen', 'salmon'])
    plt.axhline(y=1, color='r', linestyle='--', label='Ideal Efficiency')
    plt.ylabel('Efficiency (Speedup / Threads)')
    plt.title('Average Parallel Efficiency')
    plt.ylim(0, 1.2) # Efficiency is typically between 0 and 1
    plt.bar_label(bars, fmt='%.2f')

    efficiency_plot_path = os.path.join(OUTPUT_DIR, 'efficiency_comparison.png')
    plt.savefig(efficiency_plot_path)
    print(f"Saved efficiency comparison plot to '{efficiency_plot_path}'")
    plt.close()

if __name__ == '__main__':
    main()
