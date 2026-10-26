import pandas as pd
import json

df = pd.read_csv('c:/Users/bit/Documents/princy/cloud_resource_demand_dataset.csv')

with open('c:/Users/bit/Documents/princy/dataset_description.md', 'w') as f:
    f.write("# Cloud Resource Demand Prediction Dataset\n\n")
    f.write("## 1. Dataset Description\n")
    f.write("This dataset simulates realistic cloud infrastructure telemetry over a prolonged period (approx 69 days at 1-minute intervals). It is designed to train machine learning models for proactive resource auto-scaling, demand prediction, and capacity planning. The dataset includes daily and weekly seasonality, holiday effects, load spikes, and introduces complex relationships between user traffic, resource utilization (CPU, memory, network), and application performance (response time, error rates, queue lengths).\n\n")
    
    f.write("## 2. Number of Records\n")
    f.write(f"- **Total Records**: {len(df):,}\n\n")
    
    f.write("## 3. Attribute Descriptions\n")
    f.write("""
1. **timestamp**: Date and time of the observation (1-minute intervals).
2. **request_rate**: Number of HTTP/API requests received per second.
3. **active_users**: Number of currently active users.
4. **cpu_usage_percent**: CPU utilization percentage of the deployment.
5. **memory_usage_percent**: Memory/RAM utilization percentage.
6. **disk_usage_percent**: Disk utilization percentage.
7. **network_in_mbps**: Incoming network traffic in Mbps.
8. **network_out_mbps**: Outgoing network traffic in Mbps.
9. **response_time_ms**: Average application response time.
10. **error_rate_percent**: Percentage of failed requests.
11. **pod_count**: Number of running application containers/pods.
12. **container_cpu_usage**: Average CPU consumption per container.
13. **container_memory_usage**: Average Memory consumption per container.
14. **queue_length**: Number of requests waiting to be processed.
15. **workload_type**: Categorical workload level ('low', 'normal', 'medium', 'high', 'spike').
16. **hour**: Hour of the day (0-23).
17. **day_of_week**: Day of the week (0=Monday, 6=Sunday).
18. **is_weekend**: Binary flag (1 if weekend, 0 otherwise).
19. **is_holiday**: Binary flag (1 if holiday, 0 otherwise).
20. **temperature**: Simulated environmental factor affecting workload.
21. **cpu_threshold**: Static threshold used for scaling decisions.
22. **memory_threshold**: Static threshold used for scaling decisions.
23. **scaling_action**: Target action ('scale_up', 'scale_down', 'no_action').
24. **target_pod_count**: The ideal number of pods required for the next interval.
25. **future_request_rate**: Expected request rate in the next interval.
26. **future_cpu_usage**: Expected CPU usage in the next interval.
27. **future_memory_usage**: Expected Memory usage in the next interval.
28. **demand_level**: Future resource demand category ('low', 'medium', 'high', 'critical').
29. **resource_demand**: Continuous numerical target of required resources.
30. **scaling_required**: Binary target indicating if a scaling action is required (1) or not (0).
\n""")

    f.write("## 4. Data Types\n")
    f.write("| Column | Data Type |\n")
    f.write("|---|---|\n")
    for col, dtype in df.dtypes.items():
        f.write(f"| {col} | {dtype} |\n")
    f.write("\n")
    
    f.write("## 5. Missing Value Statistics\n")
    f.write("| Column | Missing Values | Percentage |\n")
    f.write("|---|---|---|\n")
    missing = df.isnull().sum()
    for col in df.columns:
        if missing[col] > 0:
            pct = (missing[col] / len(df)) * 100
            f.write(f"| {col} | {missing[col]} | {pct:.2f}% |\n")
    f.write("\n")
    
    f.write("## 6. Descriptive Statistics (Numerical Attributes)\n")
    f.write("| Column | Min | Max | Mean | Std Dev |\n")
    f.write("|---|---|---|---|---|\n")
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in num_cols:
        f.write(f"| {col} | {df[col].min():.2f} | {df[col].max():.2f} | {df[col].mean():.2f} | {df[col].std():.2f} |\n")
    f.write("\n")
    
    f.write("""## 7. Target Variables
- **scaling_required (Binary)**: Use for classification tasks to predict whether any scaling intervention is needed.
- **scaling_action (Multiclass)**: Use for multiclass classification to predict the exact direction of scaling (`scale_up`, `scale_down`, `no_action`).
- **target_pod_count (Regression)**: Use to predict the precise number of pods that should be allocated.
- **future_cpu_usage / future_memory_usage (Time-Series Forecasting)**: Direct metrics to forecast, providing inputs into a rule-based auto-scaler.

## 8. Recommended Features for Training
- **Historical Workload Features**: `request_rate`, `active_users`, `network_in_mbps`
- **Current Resource State**: `cpu_usage_percent`, `memory_usage_percent`, `pod_count`, `queue_length`, `response_time_ms`
- **Time/Temporal Features**: `hour`, `day_of_week`, `is_weekend`, `is_holiday`
- **Environmental**: `temperature`

*(Note: Ensure target variables like `future_*`, `scaling_action`, and `target_pod_count` are dropped from the input features during training to avoid data leakage.)*

## 9. Example ML Models
- **Random Forest / XGBoost / LightGBM**: Excellent for tabular modeling of `scaling_required` or `scaling_action` using engineered lag features.
- **LSTM / GRU**: Deep learning sequential models perfect for continuous forecasting of `target_pod_count` or `future_cpu_usage` using historical sequences (e.g., past 60 minutes).
- **Transformer-based (e.g., Time-Series Transformer, Informer)**: Cutting-edge models for capturing complex long-term dependencies (like daily and weekly seasonality).

## 10. Recommended Train/Validation/Test Split
To prevent data leakage in time-series forecasting, a strictly **chronological split** is required. Random splitting will allow future data points to bleed into the training set.

- **Training Set**: First 70% of the timeline (approx 48 days). Used for model learning.
- **Validation Set**: Next 15% of the timeline (approx 10 days). Used for hyperparameter tuning and early stopping.
- **Test Set**: Final 15% of the timeline (approx 11 days). Used for final evaluation to test generalization to future data.
""")

print("Markdown report generated.")
