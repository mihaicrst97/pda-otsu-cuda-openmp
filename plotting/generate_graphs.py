import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# path absolut pentru directorul cu script ul
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# construire path uri absolute
CSV_FILE_PATH = os.path.join(PROJECT_ROOT, 'images', 'output', 'results.csv')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'plotting')

def main():
    if not os.path.exists(CSV_FILE_PATH):
        print(f"Error: CSV file not found at '{CSV_FILE_PATH}'")
        print("Please run the C++ project first to generate the results.csv file.")
        return

    # creaza un folder output daca nu exista deja
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # citire date
    df = pd.read_csv(CSV_FILE_PATH)

    # calcul speedup si efficiency
    # speedup = t_cpu / t_parallel
    df['Speedup_OMP'] = df['Time_CPU_ms'] / df['Time_OMP_ms']
    df['Speedup_TBB'] = df['Time_CPU_ms'] / df['Time_TBB_ms']

    # efficiency = speedup / no of threads
    df['Efficiency_OMP'] = df['Speedup_OMP'] / df['Threads_OMP']
    df['Efficiency_TBB'] = df['Speedup_TBB'] / df['Threads_TBB']

    # calcul average metrics
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

    # comparatie timp la executare
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

    # comparatie viteza
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

    # comparatie eficienta
    plt.figure(figsize=(10, 6))
    efficiencies = [avg_metrics['Efficiency_OMP'], avg_metrics['Efficiency_TBB']]

    bars = plt.bar(parallel_methods, efficiencies, color=['lightgreen', 'salmon'])
    plt.axhline(y=1, color='r', linestyle='--', label='Ideal Efficiency')
    plt.ylabel('Efficiency (Speedup / Threads)')
    plt.title('Average Parallel Efficiency')
    plt.ylim(0, 1.2) # eficienta e intre 0 si 1 de obicei
    plt.bar_label(bars, fmt='%.2f')

    efficiency_plot_path = os.path.join(OUTPUT_DIR, 'efficiency_comparison.png')
    plt.savefig(efficiency_plot_path)
    print(f"Saved efficiency comparison plot to '{efficiency_plot_path}'")
    plt.close()

if __name__ == '__main__':
    main()
