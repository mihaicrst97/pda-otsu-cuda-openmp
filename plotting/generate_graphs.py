import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CSV_FILE_PATH = os.path.join(PROJECT_ROOT, 'images', 'output', 'results.csv')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'plotting')

def main():
    if not os.path.exists(CSV_FILE_PATH):
        print(f"Error: CSV file not found at '{CSV_FILE_PATH}'")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    df = pd.read_csv(CSV_FILE_PATH)

    # --- Calculate Speedup and Efficiency ---
    df['Speedup_OMP'] = df['Time_CPU_ms'] / df['Time_OMP_ms']
    df['Speedup_TBB'] = df['Time_CPU_ms'] / df['Time_TBB_ms']
    df['Efficiency_OMP'] = df['Speedup_OMP'] / df['Threads_OMP']
    df['Efficiency_TBB'] = df['Speedup_TBB'] / df['Threads_TBB']

    # --- 1. Average Metrics Bar Plots ---
    avg_metrics = {
        'Time_CPU': df['Time_CPU_ms'].mean(),
        'Time_OMP': df['Time_OMP_ms'].mean(),
        'Time_TBB': df['Time_TBB_ms'].mean(),
        'Speedup_OMP': df['Speedup_OMP'].mean(),
        'Speedup_TBB': df['Speedup_TBB'].mean(),
        'Efficiency_OMP': df['Efficiency_OMP'].mean(),
        'Efficiency_TBB': df['Efficiency_TBB'].mean(),
    }
    print("Average Metrics (across all runs):")
    for key, value in avg_metrics.items():
        print(f"  {key}: {value:.4f}")

    # --- Plot 1: Time Comparison ---
    plt.figure(figsize=(10, 6))
    methods = ['CPU', 'OpenMP', 'TBB']
    times = [avg_metrics['Time_CPU'], avg_metrics['Time_OMP'], avg_metrics['Time_TBB']]
    bars = plt.bar(methods, times, color=['skyblue', 'lightgreen', 'salmon'])
    plt.ylabel('Average Execution Time (ms)')
    plt.title('Average Execution Time Comparison')
    plt.bar_label(bars, fmt='%.2f ms')
    time_plot_path = os.path.join(OUTPUT_DIR, 'time_comparison.png')
    plt.savefig(time_plot_path)
    print(f"\nSaved plot to '{time_plot_path}'")
    plt.close()

    # --- Plot 2: Speedup Comparison ---
    plt.figure(figsize=(10, 6))
    parallel_methods = ['OpenMP', 'TBB']
    speedups = [avg_metrics['Speedup_OMP'], avg_metrics['Speedup_TBB']]
    bars = plt.bar(parallel_methods, speedups, color=['lightgreen', 'salmon'])
    plt.axhline(y=1, color='r', linestyle='--', label='No Speedup')
    plt.ylabel('Average Speedup Factor (vs. CPU)')
    plt.title('Average Speedup Comparison')
    plt.bar_label(bars, fmt='%.2fx')
    speedup_plot_path = os.path.join(OUTPUT_DIR, 'speedup_comparison.png')
    plt.savefig(speedup_plot_path)
    print(f"Saved plot to '{speedup_plot_path}'")
    plt.close()

    # --- Plot 3: Efficiency Comparison ---
    plt.figure(figsize=(10, 6))
    efficiencies = [avg_metrics['Efficiency_OMP'], avg_metrics['Efficiency_TBB']]
    bars = plt.bar(parallel_methods, efficiencies, color=['lightgreen', 'salmon'])
    plt.axhline(y=1, color='r', linestyle='--', label='Ideal Efficiency')
    plt.ylabel('Average Efficiency (Speedup / Threads)')
    plt.title('Average Parallel Efficiency')
    plt.ylim(0, 1.2)
    plt.bar_label(bars, fmt='%.2f')
    efficiency_plot_path = os.path.join(OUTPUT_DIR, 'efficiency_comparison.png')
    plt.savefig(efficiency_plot_path)
    print(f"Saved plot to '{efficiency_plot_path}'")
    plt.close()

    # --- Plot 4: Scalability Analysis Line Plot ---
    scalability_omp = df.groupby('Threads_OMP')['Speedup_OMP'].mean().reset_index()
    scalability_tbb = df.groupby('Threads_TBB')['Speedup_TBB'].mean().reset_index()

    plt.figure(figsize=(12, 8))
    plt.plot(scalability_omp['Threads_OMP'], scalability_omp['Speedup_OMP'], marker='o', linestyle='-', label='OpenMP Speedup')
    plt.plot(scalability_tbb['Threads_TBB'], scalability_tbb['Speedup_TBB'], marker='s', linestyle='-', label='TBB Speedup')
    
    max_threads = max(scalability_omp['Threads_OMP'].max(), scalability_tbb['Threads_TBB'].max())
    ideal_speedup_range = range(1, int(max_threads) + 2)
    plt.plot(ideal_speedup_range, ideal_speedup_range, color='red', linestyle='--', label='Ideal Speedup')

    plt.title('Scalability Analysis: Speedup vs. Number of Threads')
    plt.xlabel('Number of Threads')
    plt.ylabel('Speedup Factor (vs. CPU)')
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.xticks(np.arange(0, max_threads + 2, 2))

    scalability_plot_path = os.path.join(OUTPUT_DIR, 'scalability_vs_threads.png')
    plt.savefig(scalability_plot_path)
    print(f"Saved plot to '{scalability_plot_path}'")
    plt.close()

if __name__ == '__main__':
    main()
