
# **Exercise 3 — TensorFlow Data Validation (TFDV) Schema & Anomaly Detection**

**Notebook:** `TFDV-schema-anomoly-detection.ipynb`
**Project:** UCI Bank Marketing ML Lab
**Bucket:** `gs://uci-bank-ml-bucket/bank-additional/`
**Region:** `us-central1`

---

## **1. Overview**

This lab demonstrates how **TensorFlow Data Validation (TFDV)** can automatically profile data, infer schema domains, and detect anomalies.
Using the **Bank Additional Full dataset**, the notebook validates that feature domains and value ranges are consistent before training any ML model.

All TFDV artifacts — statistics, schema, and anomaly files — were stored in the Cloud Storage bucket for reproducibility and future monitoring.

---

## **2. Workflow Summary**

### **Step 1 — Data Source and Setup**

* Dataset: `bank-additional-full.csv`
* Loaded from: `gs://uci-bank-ml-bucket/bank-additional/`
* Supporting files uploaded to Cloud Storage:

  * `bank-additional-full_stats.stats`
  * `bank-additional-full_schema.textproto`
  * `anomalies.pbtxt`

### **Step 2 — Generate Statistics**

```python
train_stats = tfdv.generate_statistics_from_csv(
    data_location='bank-additional-full.csv',
    delimiter=';'
)
tfdv.visualize_statistics(train_stats)
```

**Output Summary:**

* Total Rows: ~41.2k
* Missing Values: 0% across all categorical features
* Feature Count: 21 columns (11 categorical visualized)
* Key observations:

  * `contact`: most frequent = cellular (26.1k)
  * `day_of_week`: distributed across mon–fri
  * `education`: 8 unique values, dominated by university.degree
  * `housing` and `loan`: binary yes/no pattern
  * `y` (target): 36.5k “no” vs 4.7k “yes”

### **Step 3 — Schema Inference**

```python
schema = tfdv.infer_schema(statistics=train_stats)
tfdv.display_schema(schema)
```

Extracted domains show expected categorical options:

| Feature   | Domain Values                                                                     |
| --------- | --------------------------------------------------------------------------------- |
| job       | admin., blue-collar, entrepreneur, housemaid, retired, services, student, unknown |
| marital   | divorced, married, single, unknown                                                |
| education | basic.4y, basic.6y, high.school, university.degree, unknown                       |
| contact   | cellular, telephone                                                               |
| month     | jan–dec (10 unique months present)                                                |
| y         | no, yes                                                                           |

---

### **Step 4 — Anomaly Detection**

```python
anomalies = tfdv.validate_statistics(statistics=train_stats, schema=schema)
tfdv.display_anomalies(anomalies)
```

**Result:** No anomalies found.
All features matched their inferred domains, indicating complete schema consistency.

---

## **3. Cloud Storage Artifacts**

| File Name                               | Purpose                                  | Location                                   |
| --------------------------------------- | ---------------------------------------- | ------------------------------------------ |
| `bank-additional-full_stats.stats`      | Feature-level statistics                 | `gs://uci-bank-ml-bucket/bank-additional/` |
| `bank-additional-full_schema.textproto` | Schema definition inferred by TFDV       | `gs://uci-bank-ml-bucket/bank-additional/` |
| `anomalies.pbtxt`                       | Final anomaly report (empty – no issues) | `gs://uci-bank-ml-bucket/bank-additional/` |
| `bank-additional-full-schema-check`     | Verification artifact                    | `gs://uci-bank-ml-bucket/bank-additional/` |

---

## **4. Observations**

* The dataset shows no missing values across all columns.
* All categorical domains are clean and well-defined.
* The target column `y` is slightly imbalanced (majority “no”).
* Schema validation confirms the dataset is healthy and ready for downstream ML pipelines.
* All outputs were successfully stored in Cloud Storage for traceability.

---

## **5. Final Outcomes**

| Validation Step         | Status                      |
| ----------------------- | --------------------------- |
| Data Loaded from GCS    | Passed                      |
| Statistics Generated    | Passed                      |
| Schema Inferred         | Passed                      |
| Anomaly Validation      | Passed (no anomalies found) |
| Artifacts Stored in GCS | Completed                   |

---

## **6. Key Learning Takeaways**

* TFDV provides quick, automated feature-level statistics and validation.
* Schema inference standardizes categorical domains and expected ranges.
* Anomaly detection ensures data quality before model training.
* Storing validation artifacts in Cloud Storage allows reproducibility and future drift checks.
* The exercise builds a strong foundation for integrating data validation into TFX or Vertex AI pipelines.
