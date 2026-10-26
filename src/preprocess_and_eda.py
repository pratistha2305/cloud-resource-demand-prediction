import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for academic/presentation quality figures
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

FIGURES_DIR = os.path.join("reports", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

def main():
    print("=" * 60)
    print("AI-POWERED CLOUD AUTO-SCALING: PREPROCESSING & EDA PIPELINE")
    print("=" * 60)

    # 1. Load Dataset
    raw_path = "cloud_resource_demand_dataset.csv"
    print(f"\n[1/5] Loading raw telemetry data from: {raw_path}")
    df = pd.read_csv(raw_path)
    print(f"      Initial shape: {df.shape[0]:,} rows, {df.shape[1]} columns")

    # Parse timestamps
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)
    print(f"      Time range: {df['timestamp'].min()} to {df['timestamp'].max()}")

    # 2. Missing Value Analysis
    print("\n[2/5] Analyzing and handling missing telemetry values...")
    missing_before = df.isnull().sum()
    missing_cols = missing_before[missing_before > 0]
    print("      Missing counts before imputation:")
    for col, count in missing_cols.items():
        print(f"        - {col:25s}: {count:5d} ({count/len(df)*100:.2f}%)")

    # Plot 1: Missing values distribution
    plt.figure(figsize=(10, 5))
    missing_pct = (missing_cols / len(df)) * 100
    bars = plt.barh(missing_pct.index, missing_pct.values, color='#e74c3c', alpha=0.85, edgecolor='black', linewidth=0.5)
    plt.xlabel('Missing Percentage (%)', fontsize=11, fontweight='bold')
    plt.title('Sensor Telemetry Missing Value Distribution Before Imputation', fontsize=13, fontweight='bold', pad=12)
    plt.xlim(0, max(missing_pct.values) * 1.25)
    for bar in bars:
        w = bar.get_width()
        plt.text(w + 0.05, bar.get_y() + bar.get_height()/2, f'{w:.2f}%', ha='left', va='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "01_missing_values_report.png"), dpi=300)
    plt.close()
    print("      Saved: reports/figures/01_missing_values_report.png")

    # Time-series imputation:
    # Sensor/continuous metrics: forward fill then linear interpolation
    continuous_sensor_cols = [
        'request_rate', 'active_users', 'cpu_usage_percent', 'memory_usage_percent',
        'disk_usage_percent', 'network_in_mbps', 'network_out_mbps', 'response_time_ms',
        'error_rate_percent', 'container_cpu_usage', 'container_memory_usage',
        'queue_length', 'environmental_factor'
    ]
    for col in continuous_sensor_cols:
        if col in df.columns:
            df[col] = df[col].interpolate(method='linear').bfill().ffill()

    # Drop the trailing 5 rows where future 5-minute lookahead targets have no future data
    df_clean = df.dropna().copy().reset_index(drop=True)
    print(f"      Shape after imputation and trimming boundary rows: {df_clean.shape[0]:,} rows")
    assert df_clean.isnull().sum().sum() == 0, "Missing values still remain!"
    print("      Verified: 0 missing values remaining across all columns!")

    # Save Cleaned Dataset
    clean_csv_path = "cleaned_cloud_resource_demand_dataset.csv"
    df_clean.to_csv(clean_csv_path, index=False)
    print(f"      Saved cleaned dataset to: {clean_csv_path}")

    # 3. Exploratory Data Analysis (EDA) & Visualizations
    print("\n[3/5] Generating publication-quality EDA figures...")

    # Plot 2: Seasonality (Hourly & Weekly)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Hourly diurnal profile
    hourly_stats = df_clean.groupby('hour')[['request_rate', 'cpu_usage_percent']].mean()
    hourly_std = df_clean.groupby('hour')[['request_rate', 'cpu_usage_percent']].std()
    
    color_req = '#2980b9'
    ax1.plot(hourly_stats.index, hourly_stats['request_rate'], color=color_req, marker='o', linewidth=2.5, label='Request Rate (req/s)')
    ax1.fill_between(hourly_stats.index, hourly_stats['request_rate'] - hourly_std['request_rate']*0.3,
                     hourly_stats['request_rate'] + hourly_std['request_rate']*0.3, color=color_req, alpha=0.15)
    ax1.set_xlabel('Hour of Day (0 - 23 UTC)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Mean Request Rate (req/s)', color=color_req, fontsize=11, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=color_req)
    ax1.set_title('Diurnal (24-Hour) Workload Cycle', fontsize=12, fontweight='bold')
    ax1.set_xticks(range(0, 24, 2))
    ax1.grid(True, linestyle='--', alpha=0.5)

    ax1_twin = ax1.twinx()
    color_cpu = '#e67e22'
    ax1_twin.plot(hourly_stats.index, hourly_stats['cpu_usage_percent'], color=color_cpu, marker='s', linewidth=2, linestyle='--', label='CPU %')
    ax1_twin.set_ylabel('Mean CPU Utilization (%)', color=color_cpu, fontsize=11, fontweight='bold')
    ax1_twin.tick_params(axis='y', labelcolor=color_cpu)
    ax1_twin.grid(False)

    # Weekly profile
    day_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    weekly_stats = df_clean.groupby('day_of_week')[['request_rate', 'active_users']].mean()
    ax2.bar(day_labels, weekly_stats['request_rate'], color=['#34495e']*5 + ['#95a5a6']*2, edgecolor='black', linewidth=0.5)
    ax2.set_xlabel('Day of Week', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Mean Request Rate (req/s)', fontsize=11, fontweight='bold')
    ax2.set_title('Weekly Seasonality (Weekday vs Weekend Traffic)', fontsize=12, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "02_seasonality_patterns.png"), dpi=300)
    plt.close()
    print("      Saved: reports/figures/02_seasonality_patterns.png")

    # Plot 3: Workload vs Resource Pressure (Scatter & Density)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    sample_sub = df_clean.sample(n=5000, random_state=42)

    ax1.scatter(sample_sub['active_users'], sample_sub['request_rate'], alpha=0.25, color='#3498db', s=15, edgecolors='none')
    m1, b1 = np.polyfit(sample_sub['active_users'], sample_sub['request_rate'], 1)
    ax1.plot(sample_sub['active_users'], m1*sample_sub['active_users'] + b1, color='#c0392b', linewidth=2, label=f'Trend (Slope: {m1:.3f})')
    ax1.set_xlabel('Active Users', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Incoming Request Rate (req/s)', fontsize=11, fontweight='bold')
    ax1.set_title('Workload Driver: Active Users vs Request Rate', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper left')
    ax1.grid(True, linestyle='--', alpha=0.5)

    ax2.scatter(sample_sub['request_rate'], sample_sub['cpu_usage_percent'], alpha=0.25, color='#9b59b6', s=15, edgecolors='none')
    m2, b2 = np.polyfit(sample_sub['request_rate'], sample_sub['cpu_usage_percent'], 1)
    ax2.plot(sample_sub['request_rate'], m2*sample_sub['request_rate'] + b2, color='#e74c3c', linewidth=2, label=f'Trend (Slope: {m2:.3f})')
    ax2.axhline(80, color='#d35400', linestyle='--', linewidth=1.5, label='Scaling Threshold (80% CPU)')
    ax2.set_xlabel('Request Rate (req/s)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('CPU Utilization (%)', fontsize=11, fontweight='bold')
    ax2.set_title('System Saturation: Request Rate vs Fleet CPU %', fontsize=12, fontweight='bold')
    ax2.legend(loc='lower right')
    ax2.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "03_workload_resource_relationship.png"), dpi=300)
    plt.close()
    print("      Saved: reports/figures/03_workload_resource_relationship.png")

    # Plot 4: Demonstrating Reactive Auto-Scaler Lag During Traffic Surges (24-Hour Snippet)
    # Pick a 24-hour window with spike
    spike_day = df_clean[df_clean['workload_type'] == 'spike'].iloc[10]['timestamp'].floor('D')
    window = df_clean[(df_clean['timestamp'] >= spike_day) & (df_clean['timestamp'] < spike_day + pd.Timedelta(days=1))].copy()
    if len(window) < 1000:
        window = df_clean.iloc[1440*2 : 1440*3].copy()

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 9), sharex=True)

    ax1.plot(window['timestamp'], window['request_rate'], color='#2980b9', linewidth=1.8, label='Request Rate (req/s)')
    ax1.set_ylabel('Workload (req/s)', fontsize=10, fontweight='bold')
    ax1.set_title(f'Telemetry Trace & Reactive Auto-Scaling Dynamics ({window["timestamp"].dt.date.iloc[0]})', fontsize=13, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(True, linestyle='--', alpha=0.5)

    ax2.plot(window['timestamp'], window['cpu_usage_percent'], color='#e74c3c', linewidth=1.5, label='CPU Usage %')
    ax2.axhline(80, color='darkred', linestyle='--', linewidth=1.2, label='CPU Scale Threshold (80%)')
    ax2.set_ylabel('CPU Saturation (%)', fontsize=10, fontweight='bold')
    ax2.legend(loc='upper right')
    ax2.grid(True, linestyle='--', alpha=0.5)

    ax3.step(window['timestamp'], window['pod_count'], color='#27ae60', where='post', linewidth=2.2, label='Current Active Pods')
    ax3.step(window['timestamp'], window['target_pod_count'], color='#8e44ad', where='post', linestyle=':', linewidth=1.8, label='Target Pods (Required)')
    ax3.set_ylabel('Fleet Pod Count', fontsize=10, fontweight='bold')
    ax3.set_xlabel('Timestamp (UTC)', fontsize=10, fontweight='bold')
    ax3.legend(loc='upper right')
    ax3.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "04_reactive_scaling_lag.png"), dpi=300)
    plt.close()
    print("      Saved: reports/figures/04_reactive_scaling_lag.png")

    # Plot 5: QoS & SLA Impact (Response Time and Errors across Workload Types)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    workload_order = ['low', 'normal', 'medium', 'high', 'spike']
    workload_present = [w for w in workload_order if w in df_clean['workload_type'].unique()]

    sns.boxplot(data=df_clean, x='workload_type', y='response_time_ms', order=workload_present,
                palette='Blues', ax=ax1, showfliers=False)
    ax1.set_title('Application Latency (Response Time) vs Workload Type', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Workload Type', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Response Time (ms)', fontsize=11, fontweight='bold')
    ax1.grid(True, linestyle='--', alpha=0.5)

    sns.boxplot(data=df_clean, x='workload_type', y='error_rate_percent', order=workload_present,
                palette='Reds', ax=ax2, showfliers=False)
    ax2.set_title('Error Rate % vs Workload Type (SLA Stress)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Workload Type', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Error Rate (%)', fontsize=11, fontweight='bold')
    ax2.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "05_sla_and_latency_stress.png"), dpi=300)
    plt.close()
    print("      Saved: reports/figures/05_sla_and_latency_stress.png")

    # Plot 6: Correlation Heatmap
    corr_cols = [
        'request_rate', 'active_users', 'cpu_usage_percent', 'memory_usage_percent',
        'network_in_mbps', 'network_out_mbps', 'response_time_ms', 'error_rate_percent',
        'pod_count', 'queue_length', 'future_cpu_usage', 'future_request_rate', 'resource_demand'
    ]
    corr_matrix = df_clean[corr_cols].corr()

    plt.figure(figsize=(11, 9))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1,
                linewidths=0.5, cbar_kws={'label': 'Pearson Correlation'})
    plt.title('Correlation Matrix: Telemetry, System Resources & Forward Demand', fontsize=13, fontweight='bold', pad=14)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "06_correlation_heatmap.png"), dpi=300)
    plt.close()
    print("      Saved: reports/figures/06_correlation_heatmap.png")

    print("\n[4/5] Preprocessing & EDA Summary Report:")
    print(f"      - Total Records: {len(df_clean):,}")
    print(f"      - Cleaned Dataset: {clean_csv_path}")
    print(f"      - Figures Saved: 6 visual charts in {FIGURES_DIR}")

    print("\n[5/5] Pipeline successfully completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
