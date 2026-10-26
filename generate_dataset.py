import pandas as pd
import numpy as np
import datetime
import os
import json

def generate_data(num_records=100000):
    np.random.seed(42)
    
    # 1. timestamp
    start_date = datetime.datetime(2023, 1, 1, 0, 0, 0)
    timestamps = [start_date + datetime.timedelta(minutes=i) for i in range(num_records)]
    
    df = pd.DataFrame({'timestamp': timestamps})
    
    # Time features
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # Holidays (random 5 days)
    holiday_dates = np.random.choice(pd.date_range(start='2023-01-01', periods=100).date, 5, replace=False)
    df['is_holiday'] = df['timestamp'].dt.date.isin(holiday_dates).astype(int)
    
    # Base workload pattern (Daily and Weekly seasonality)
    daily_seasonality = np.sin((df['hour'] - 6) * (2 * np.pi / 24)) * 0.5 + 0.5
    weekly_seasonality = np.where(df['is_weekend'], 0.6, 1.0)
    holiday_effect = np.where(df['is_holiday'], 0.5, 1.0)
    
    base_multiplier = daily_seasonality * weekly_seasonality * holiday_effect
    
    # Active Users
    df['active_users'] = np.maximum(100, (base_multiplier * 5000 + np.random.normal(0, 200, num_records))).astype(int)
    
    # Spikes (2% of the time)
    spike_indices = np.random.rand(num_records) < 0.02
    df.loc[spike_indices, 'active_users'] = (df.loc[spike_indices, 'active_users'] * np.random.uniform(1.5, 3.0)).astype(int)
    
    # Request Rate (Requests per second)
    df['request_rate'] = np.maximum(10, df['active_users'] * 0.1 + np.random.normal(0, 10, num_records))
    
    # Determine Workload Type
    def get_workload_type(users, is_spike):
        if is_spike: return 'spike'
        if users > 4000: return 'high'
        if users > 2000: return 'medium'
        if users > 800: return 'normal'
        return 'low'
    
    df['workload_type'] = [get_workload_type(u, s) for u, s in zip(df['active_users'], spike_indices)]
    
    # Temperature (dummy environmental factor)
    df['temperature'] = 20 + np.sin((df['hour'] - 12) * (2 * np.pi / 24)) * 10 + np.random.normal(0, 2, num_records)
    
    # Pods (Dynamic scaling logic with some lag)
    # Target pods based on active users (1 pod per 500 users)
    ideal_pods = np.ceil(df['active_users'] / 500.0).astype(int)
    ideal_pods = np.maximum(2, ideal_pods) # minimum 2 pods
    
    # Smooth the pod count to simulate scaling delay
    pod_count = np.zeros(num_records)
    pod_count[0] = ideal_pods[0]
    for i in range(1, num_records):
        if ideal_pods[i] > pod_count[i-1]:
            pod_count[i] = pod_count[i-1] + min(2, ideal_pods[i] - pod_count[i-1]) # Scale up slowly
        elif ideal_pods[i] < pod_count[i-1]:
            pod_count[i] = pod_count[i-1] - min(1, pod_count[i-1] - ideal_pods[i]) # Scale down slower
        else:
            pod_count[i] = pod_count[i-1]
    
    df['pod_count'] = pod_count.astype(int)
    
    # Resource Usage
    cpu_per_user = 0.015
    mem_per_user = 0.012
    
    total_cpu_needed = df['active_users'] * cpu_per_user
    total_mem_needed = df['active_users'] * mem_per_user
    
    df['cpu_usage_percent'] = np.clip((total_cpu_needed / df['pod_count']) + np.random.normal(5, 2, num_records), 5, 99)
    df['memory_usage_percent'] = np.clip((total_mem_needed / df['pod_count']) + np.random.normal(10, 2, num_records), 10, 99)
    
    df['container_cpu_usage'] = df['cpu_usage_percent'] * 0.9 + np.random.normal(0, 1, num_records)
    df['container_memory_usage'] = df['memory_usage_percent'] * 0.9 + np.random.normal(0, 1, num_records)
    
    df['disk_usage_percent'] = np.clip(40 + (df['hour'] / 24) * 10 + np.random.normal(0, 1, num_records), 10, 95)
    
    # Network
    df['network_in_mbps'] = np.maximum(1, df['request_rate'] * 0.5 + np.random.normal(0, 2, num_records))
    df['network_out_mbps'] = np.maximum(5, df['request_rate'] * 2.0 + np.random.normal(0, 5, num_records))
    
    # Performance metrics
    load_factor = df['cpu_usage_percent'] / 100.0
    df['response_time_ms'] = np.maximum(50, 50 + (load_factor**3) * 500 + np.random.normal(0, 10, num_records))
    
    df['queue_length'] = np.where(df['cpu_usage_percent'] > 85, np.random.randint(10, 100, num_records), np.random.randint(0, 5, num_records))
    df['error_rate_percent'] = np.where(df['cpu_usage_percent'] > 90, np.random.uniform(1, 5, num_records), np.random.uniform(0, 0.1, num_records))
    
    # Thresholds
    df['cpu_threshold'] = 80.0
    df['memory_threshold'] = 80.0
    
    # Future features (Next interval = +1 step)
    df['future_request_rate'] = df['request_rate'].shift(-1).fillna(method='ffill')
    df['future_cpu_usage'] = df['cpu_usage_percent'].shift(-1).fillna(method='ffill')
    df['future_memory_usage'] = df['memory_usage_percent'].shift(-1).fillna(method='ffill')
    
    # Target variables
    df['target_pod_count'] = df['pod_count'].shift(-1).fillna(method='ffill')
    
    def get_scaling_action(current, target):
        if target > current: return 'scale_up'
        if target < current: return 'scale_down'
        return 'no_action'
    
    df['scaling_action'] = [get_scaling_action(c, t) for c, t in zip(df['pod_count'], df['target_pod_count'])]
    
    def get_demand_level(cpu):
        if cpu > 85: return 'critical'
        if cpu > 70: return 'high'
        if cpu > 40: return 'medium'
        return 'low'
        
    df['demand_level'] = [get_demand_level(c) for c in df['future_cpu_usage']]
    df['resource_demand'] = df['future_cpu_usage'] * 0.6 + df['future_memory_usage'] * 0.4
    df['scaling_required'] = (df['scaling_action'] != 'no_action').astype(int)
    
    # Introduce missing values (0.5% missing in some columns)
    missing_cols = ['cpu_usage_percent', 'memory_usage_percent', 'response_time_ms', 'network_in_mbps']
    for col in missing_cols:
        mask = np.random.rand(num_records) < 0.005
        df.loc[mask, col] = np.nan
        
    # Reorder columns to match request
    cols = ['timestamp', 'request_rate', 'active_users', 'cpu_usage_percent', 'memory_usage_percent',
            'disk_usage_percent', 'network_in_mbps', 'network_out_mbps', 'response_time_ms', 'error_rate_percent',
            'pod_count', 'container_cpu_usage', 'container_memory_usage', 'queue_length', 'workload_type',
            'hour', 'day_of_week', 'is_weekend', 'is_holiday', 'temperature', 'cpu_threshold', 'memory_threshold',
            'scaling_action', 'target_pod_count', 'future_request_rate', 'future_cpu_usage', 'future_memory_usage',
            'demand_level', 'resource_demand', 'scaling_required']
    
    df = df[cols]
    
    # Write to CSV
    csv_path = 'c:/Users/bit/Documents/princy/cloud_resource_demand_dataset.csv'
    df.to_csv(csv_path, index=False)
    
    # Generate Stats
    stats = {}
    stats['num_records'] = len(df)
    stats['dtypes'] = df.dtypes.astype(str).to_dict()
    stats['missing'] = df.isnull().sum().to_dict()
    
    num_cols = df.select_dtypes(include=[np.number]).columns
    stats['describe'] = df[num_cols].describe().to_dict()
    
    with open('c:/Users/bit/Documents/princy/dataset_stats.json', 'w') as f:
        json.dump(stats, f)

if __name__ == '__main__':
    generate_data(100000)
    print("Dataset generated successfully.")
