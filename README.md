# AI-Powered Cloud Resource Demand Prediction and Auto-Scaling System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Time--Series-orange.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

An end-to-end intelligent cloud infrastructure management framework designed to predict future computing resource demand (CPU, memory, request volume) and perform proactive, predictive auto-scaling.

Traditional reactive auto-scalers (e.g., standard Kubernetes Horizontal Pod Autoscaler) only scale *after* traffic surges breach resource thresholds, leading to temporary service degradation, queue buildup, and SLA violations. This system utilizes time-series machine learning models to anticipate workload surges **5 minutes ahead**, allocating pods proactively before traffic arrives.

---

## 📌 Project Architecture

```
[ Incoming Telemetry Stream ]
             │
             ▼
[ Feature Engineering & Lag Pipeline ]
   • Rolling 5m/15m/1h aggregations
   • Cyclical diurnal & weekly encoding
             │
             ▼
[ Predictive AI Engine ] (LSTM / GRU / XGBoost)
   • Predicts future CPU & request volume (t + 5m)
   • Forecasts required pod counts
             │
             ▼
[ Proactive Auto-Scaler Controller ]
   • Evaluates safety margins & cooldown policies
   • Triggers proactive Pod scale-up / scale-down
             │
             ▼
[ Container / Pod Cluster ]
```

---

## 📊 Dataset Overview

The project includes a realistically simulated cloud telemetry dataset representing ~46.5 days of enterprise application traffic at 1-minute resolution:

- **Filename:** `cloud_resource_demand_dataset.csv`
- **Volume:** ~67,000+ timestamped telemetry records
- **Dimensions:** 30 comprehensive features
- **Key Attributes:**
  - **Traffic Metrics:** `request_rate`, `active_users`, `network_in_mbps`, `network_out_mbps`
  - **System Saturation:** `cpu_usage_percent`, `memory_usage_percent`, `disk_usage_percent`, `pod_count`
  - **Quality of Service (QoS):** `response_time_ms`, `error_rate_percent`, `queue_length`
  - **Temporal & Environmental:** `hour`, `day_of_week`, `is_weekend`, `is_holiday`, `environmental_factor`
  - **Forward-Looking Target Variables (5 min lookahead):** `future_cpu_usage`, `future_request_rate`, `target_pod_count`, `scaling_action`, `scaling_required`

---

## 🚀 Key Modules & Roadmap

- [x] **Phase 1: Telemetry Dataset Generation & Modeling**
  - Synthesized multi-week telemetry with diurnal, weekly, and sudden burst patterns.
  - Injected realistic telemetry sensor missingness (~1.5%) for preprocessing evaluation.
- [ ] **Phase 2: Exploratory Data Analysis & Preprocessing**
  - Time-series forward imputation and linear interpolation.
  - Decomposition of seasonality, trend, and stochastic residual noise.
- [ ] **Phase 3: Time-Series Feature Engineering**
  - Multi-horizon lag features ($t-1, t-5, t-15, t-30$).
  - Chronological 70% / 15% / 15% train-validation-test partitioning (zero lookahead leakage).
- [ ] **Phase 4: Predictive Model Benchmarking**
  - Baseline Regressors vs. Random Forest, XGBoost, and Deep Sequential Models (LSTM / GRU).
- [ ] **Phase 5: Auto-Scaling Policy Simulation**
  - Direct comparative benchmarking of Reactive HPA vs. Proactive Predictive Autoscaling.
  - Evaluation of SLA breaches and resource provisioning efficiency.
- [ ] **Phase 6: Interactive Telemetry & Auto-Scaling Dashboard**
  - Streamlit dashboard displaying live predicted demand, pod fleet adjustments, and alerts.

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/cloud-resource-demand-prediction.git
   cd cloud-resource-demand-prediction
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows PowerShell:
   .venv\Scripts\Activate.ps1
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
