# Cloud Resource Demand Prediction & Auto-Scaling Dataset

## 1. Dataset Description

This is a synthetic but realistically-modeled time-series dataset simulating a cloud
application's infrastructure telemetry over **~46.5 days at 1-minute resolution**
(January 1, 2026 onward). It was generated with a physics-inspired simulator (not
pure random noise): active users drive request rate, request rate drives CPU/memory
via a simulated pod fleet with a **stateful reactive auto-scaler** (thresholds +
cooldowns + hysteresis), and downstream metrics (latency, errors, queueing, network)
are derived from that same saturation state. Daily/weekly seasonality, holidays,
random traffic spikes/dips, a slow multi-week growth trend, and injected missing
values / outliers are layered on top so the data behaves like a real observability
export rather than a clean textbook curve.

- **File:** `cloud_resource_demand_dataset.csv`
- **Number of records:** 67,000
- **Number of columns:** 30
- **Time range:** 2026-01-01 00:00:00 → 2026-02-16 15:19:00 (1-minute intervals)
- **Format:** CSV, UTF-8, header row, `timestamp` as `YYYY-MM-DD HH:MM:SS`

---

## 2. Column Descriptions

| # | Column | Type | Description |
|---|--------|------|-------------|
| 1 | `timestamp` | string (datetime) | Observation time, 1-minute cadence |
| 2 | `request_rate` | float | Incoming HTTP/API requests per second |
| 3 | `active_users` | int | Concurrently active users driving traffic |
| 4 | `cpu_usage_percent` | float | Aggregate CPU utilization of the fleet (0–100) |
| 5 | `memory_usage_percent` | float | Aggregate memory utilization (0–100), slower-moving than CPU |
| 6 | `disk_usage_percent` | float | Disk utilization (0–100), long-term growth + periodic cleanups |
| 7 | `network_in_mbps` | float | Inbound network throughput |
| 8 | `network_out_mbps` | float | Outbound network throughput |
| 9 | `response_time_ms` | float | Average application response time |
| 10 | `error_rate_percent` | float | Percentage of failed requests |
| 11 | `pod_count` | int | Currently running pods/containers (state of the simulated auto-scaler) |
| 12 | `container_cpu_usage` | float | Per-pod CPU consumption (noisy variant of #4) |
| 13 | `container_memory_usage` | float | Per-pod memory consumption (noisy variant of #5) |
| 14 | `queue_length` | float | Requests waiting to be processed |
| 15 | `workload_type` | categorical | `low`, `medium`, `normal`, `high`, or `spike` |
| 16 | `hour` | int | Hour of day (0–23) |
| 17 | `day_of_week` | int | Day of week (0=Monday … 6=Sunday) |
| 18 | `is_weekend` | binary | 1 if Saturday/Sunday |
| 19 | `is_holiday` | binary | 1 on simulated holiday dates |
| 20 | `environmental_factor` | float | External demand index (e.g. marketing/seasonal effects), 0–100 |
| 21 | `cpu_threshold` | float | CPU % threshold used by the auto-scaler at that instant |
| 22 | `memory_threshold` | float | Memory % threshold used by the auto-scaler at that instant |
| 23 | `scaling_action` | categorical | Action actually taken **now**: `scale_up`, `scale_down`, `no_action` |
| 24 | `target_pod_count` | int | Pod count after the scaling action |
| 25 | `future_request_rate` | float | Request rate **5 minutes ahead** (forecast target) |
| 26 | `future_cpu_usage` | float | CPU utilization 5 minutes ahead (forecast target) |
| 27 | `future_memory_usage` | float | Memory utilization 5 minutes ahead (forecast target) |
| 28 | `demand_level` | categorical | Forward-looking demand bucket: `low`/`medium`/`high`/`critical` |
| 29 | `resource_demand` | float | Composite 0–100 forward-looking resource pressure score |
| 30 | `scaling_required` | binary | 1 if scaling **will be** needed 5 minutes ahead, else 0 |

**Design note — two families of targets:**
`scaling_action`/`target_pod_count` are *reactive* (what the simulated system did
right now); `future_*`, `demand_level`, `resource_demand`, and `scaling_required`
are *predictive* (what will be true 5 minutes from now). Use the reactive columns
as **features**, and the predictive columns as **labels** — this is what enables
proactive, before-the-fact auto-scaling rather than reactive scaling.

---

## 3. Data Types

| Column | Dtype |
|---|---|
| timestamp | object (string, parse as datetime) |
| request_rate, active_users, cpu_usage_percent, memory_usage_percent, disk_usage_percent, network_in_mbps, network_out_mbps, response_time_ms, error_rate_percent, container_cpu_usage, container_memory_usage, queue_length, environmental_factor, cpu_threshold, memory_threshold, future_request_rate, future_cpu_usage, future_memory_usage, resource_demand | float64 |
| pod_count, hour, day_of_week, is_weekend, is_holiday, target_pod_count | int64 |
| workload_type, scaling_action, demand_level | object (categorical string) |
| scaling_required | float64 (binary 0/1, float because of trailing NaNs) |

---

## 4. Missing-Value Statistics

Missingness was injected at ~1.5% into ten "sensor-style" columns (simulating
telemetry collection gaps), plus a handful of unavoidable `NaN`s in the last 5 rows
of every forward-looking column (there is no "5 minutes ahead" for the very end of
the series).

| Column | Missing count | Missing % |
|---|---|---|
| request_rate | 1,033 | 1.542% |
| active_users | 971 | 1.449% |
| cpu_usage_percent | 1,009 | 1.506% |
| memory_usage_percent | 1,002 | 1.496% |
| disk_usage_percent | 1,007 | 1.503% |
| network_in_mbps | 1,003 | 1.497% |
| network_out_mbps | 982 | 1.466% |
| response_time_ms | 999 | 1.491% |
| error_rate_percent | 988 | 1.475% |
| queue_length | 1,011 | 1.509% |
| future_request_rate / future_cpu_usage / future_memory_usage / demand_level / resource_demand / scaling_required | 5 each | 0.007% |
| all other columns | 0 | 0.000% |

In addition, **~0.4% of rows (≈268 rows)** contain injected outliers/anomalies
(sudden CPU/latency/error/network spikes beyond what the underlying simulation
would normally produce) so the dataset supports anomaly-detection exercises, not
just clean forecasting.

---

## 5. Numerical Summary Statistics (min / max / mean / std)

| Column | min | max | mean | std |
|---|---|---|---|---|
| request_rate | 38.74 | 17,092.83 | 1,237.90 | 1,201.89 |
| active_users | 125 | 25,338 | 2,250.36 | 2,150.46 |
| cpu_usage_percent | 5.43 | 100.00 | 54.46 | 23.63 |
| memory_usage_percent | 32.74 | 100.00 | 65.39 | 11.79 |
| disk_usage_percent | 5.00 | 44.36 | 18.78 | 15.30 |
| network_in_mbps | 0.43 | 395.42 | 21.86 | 22.07 |
| network_out_mbps | 1.36 | 1,471.27 | 84.15 | 84.75 |
| response_time_ms | 28.72 | 7,049.77 | 94.72 | 257.18 |
| error_rate_percent | 0.05 | 20.08 | 0.16 | 0.42 |
| pod_count | 3 | 60 | 39.39 | 21.45 |
| container_cpu_usage | 5.37 | 100.00 | 54.25 | 23.52 |
| container_memory_usage | 29.33 | 100.00 | 65.36 | 12.37 |
| queue_length | 0.00 | 4,063.07 | 17.87 | 123.85 |
| environmental_factor | 0.00 | 41.86 | 22.03 | 7.30 |
| cpu_threshold | 63.79 | 76.52 | 69.99 | 1.50 |
| memory_threshold | 68.02 | 81.63 | 75.00 | 1.50 |
| future_request_rate | 38.74 | 17,092.83 | 1,238.15 | 1,202.53 |
| future_cpu_usage | 5.43 | 100.00 | 54.44 | 23.62 |
| future_memory_usage | 32.74 | 100.00 | 65.39 | 11.79 |
| resource_demand | 13.74 | 100.00 | 46.47 | 14.70 |
| scaling_required (binary) | 0 | 1 | 0.271 | 0.444 |

Categorical distributions:
- **workload_type:** normal 19,047 · medium 19,049 · high 15,874 · low 9,524 · spike 3,506
- **scaling_action:** no_action 63,086 · scale_up 2,289 · scale_down 1,625
- **demand_level:** medium 41,666 · high 10,878 · critical 7,000 · low 7,451 (5 NaN at series end)

All bounded quantities (`cpu_usage_percent`, `memory_usage_percent`,
`disk_usage_percent`, `container_cpu_usage`, `container_memory_usage`,
`error_rate_percent`) are strictly clipped to `[0, 100]`. All counts/rates
(`request_rate`, `active_users`, `pod_count`, `network_in_mbps`,
`network_out_mbps`, `queue_length`) are strictly `≥ 0`. No impossible values are
present outside of intentional `NaN`s.

---

## 6. Target Variables Explained

This dataset supports **three complementary modeling tasks**, all forward-looking
(predict 5 minutes ahead of the current row):

1. **Regression — `resource_demand`** (0–100 continuous score)
   A composite index (`0.40·future_cpu + 0.35·future_memory + 0.25·normalized future_request_rate`)
   representing overall infrastructure pressure in the near future. Good primary
   regression target for an LSTM/GRU/Transformer or gradient-boosted regressor.

2. **Classification — `demand_level`** (`low` / `medium` / `high` / `critical`)
   A bucketed version of the same forward-looking pressure, useful for a
   simpler classifier or as an interpretable business-facing output
   ("infra will be under `high` load in 5 minutes").

3. **Binary classification — `scaling_required`** (0/1)
   Directly answers the auto-scaling question: "will the system need to scale
   (up or down against threshold) 5 minutes from now?" This is the most directly
   actionable target for triggering **proactive** scaling before saturation
   happens, as opposed to `scaling_action`, which only tells you what the
   reactive scaler already did.

You can also train **multi-step regressors** directly on `future_request_rate`,
`future_cpu_usage`, and `future_memory_usage` as auxiliary/multi-task targets,
which tends to improve the shared representation for the primary targets above.

---

## 7. Recommended Features for Model Training

**Strong direct predictors:**
`request_rate`, `active_users`, `cpu_usage_percent`, `memory_usage_percent`,
`queue_length`, `response_time_ms`, `network_in_mbps`, `network_out_mbps`,
`pod_count`, `container_cpu_usage`, `container_memory_usage`, `error_rate_percent`

**Context / seasonality features:**
`hour`, `day_of_week`, `is_weekend`, `is_holiday`, `environmental_factor`,
`workload_type` (one-hot or target-encoded)

**Auto-scaler state (useful for the model to learn scaler behavior itself):**
`cpu_threshold`, `memory_threshold`, `scaling_action` (lagged, i.e. only the
*past* action, never the current-row action, should be a feature — see leakage
note below), `target_pod_count` (lagged)

**Recommended engineered features (not in the raw file, easy to add):**
- Rolling means/std of `request_rate`, `cpu_usage_percent`, `memory_usage_percent` over 5/15/60-minute windows
- Lag features (t-1, t-5, t-15, t-60 minutes) of the core metrics
- Rate-of-change / first differences of `request_rate` and `cpu_usage_percent` (spike detectors)
- Cyclical encodings of `hour` and `day_of_week` (sin/cos) instead of raw integers

**⚠️ Leakage warning:** Do **not** use `future_request_rate`, `future_cpu_usage`,
`future_memory_usage`, `demand_level`, `resource_demand`, or `scaling_required`
as input features — these are the labels (or derived directly from them).

---

## 8. Recommended Prediction Target

For a first model, use **`scaling_required`** (binary) or **`resource_demand`**
(continuous regression) as the primary target, with `demand_level` as a secondary/
interpretability output. This directly matches the stated objective: *predict
future cloud resource demand before the workload arrives, and trigger proactive
auto-scaling.*

---

## 9. Example ML Models Suitable for This Dataset

| Model type | Why it fits |
|---|---|
| **Random Forest / Extra Trees** | Strong baseline, handles missing values (after imputation) and non-linear thresholds well, fast to iterate |
| **XGBoost / LightGBM / CatBoost** | Best tabular baseline for `resource_demand` regression and `scaling_required` classification given the engineered lag/rolling features |
| **LSTM / GRU** | Naturally model the sequential dependence (memory's slow dynamics, queue build-up) using raw sequences without manual lag features |
| **Temporal Convolutional Network (TCN)** | Efficient alternative to LSTM/GRU for long sequences with the daily/weekly seasonality present here |
| **Transformer-based time-series models (e.g. Temporal Fusion Transformer, Informer, PatchTST)** | Best suited to capture multi-scale seasonality (daily + weekly) plus irregular spike events over long look-back windows |
| **Prophet / SARIMAX** | Good classical baselines specifically for `request_rate`/`active_users` seasonality decomposition, useful as a feature generator even if not the final model |

---

## 10. Recommended Train / Validation / Test Split (chronological)

Because this is time-series data, splits must be **chronological**, never
shuffled, to avoid leaking future information into training:

- **Train:** first 70% of rows → 2026-01-01 00:00 → ~2026-02-04 (≈46,900 rows)
- **Validation:** next 15% → ~2026-02-04 → ~2026-02-11 (≈10,050 rows)
- **Test:** final 15% → ~2026-02-11 → 2026-02-16 (≈10,050 rows)

Recommended practice:
- Use a **rolling-origin / walk-forward validation** scheme in addition to the
  single split above, especially if tuning hyperparameters, to confirm the model
  generalizes across different weeks and not just one validation window.
- Leave a small **gap (e.g. the 5-minute prediction horizon)** between the end
  of train and the start of validation/test so no label in validation window
  was computed from a feature row that leaked across the boundary.
- Fit any scaler/imputer **only on the training split**, then apply to
  validation/test, to avoid distribution leakage.

---

## 11. Files in This Delivery

- `cloud_resource_demand_dataset.csv` — the 67,000-row dataset described above
- `dataset_documentation.md` — this document
