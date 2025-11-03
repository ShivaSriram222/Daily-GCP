
# **Exercise 2 — Data Ingestion: Upload to Cloud Storage and Register BigQuery Table**

**Challenge Notebook:** `Day2_DataIngestion.ipynb`
**Theme:** Data Management and Integration on GCP
**Project:** UCI Bank Marketing ML Lab
**Region:** `us-central1`
**Bucket:** `uci-bank-ml-bucket`
**Dataset:** `bank_data`
**Table:** `uci_bank_marketing`

---

## **Overview**

This exercise demonstrates the data ingestion workflow on Google Cloud Platform (GCP), showing how data moves from local storage to **Cloud Storage**, and then to **BigQuery**.

All resources were created using the **GCP UI Console** for clarity and traceability.
The notebook serves as a verification artifact—ensuring that all resources exist, are correctly configured, and are accessible for downstream analytics and ML workflows.

---

## **Step Summary**

| **Step** | **Action**                                                  | **Tool Used**             | **Outcome**                                                                             |
| -------- | ----------------------------------------------------------- | ------------------------- | --------------------------------------------------------------------------------------- |
| 1        | Created bucket `uci-bank-ml-bucket` in `us-central1`        | GCP Console               | Verified in UI and via `gsutil ls`                                                      |
| 2        | Uploaded three source files under `bank-additional/` folder | GCP Console               | Uploaded `bank-additional-full.csv`, `bank-additional.csv`, `bank-additional-names.txt` |
| 3        | Verified bucket contents                                    | Cloud Shell (`gsutil ls`) | All files accessible                                                                    |
| 4        | Created dataset `bank_data`                                 | BigQuery UI               | Dataset created successfully                                                            |
| 5        | Registered table `uci_bank_marketing`                       | BigQuery UI (via GCS CSV) | Auto schema detection successful                                                        |
| 6        | Verified dataset and table existence                        | Notebook (Python Client)  | Verified successfully                                                                   |
| 7        | Executed verification queries                               | BigQuery Console          | All queries ran successfully                                                            |
| 8        | Saved query outputs and screenshots                         | BigQuery Console          | Results documented for review                                                           |

---

## **Verification Queries**

### 1. Row Count and Label Balance (`verify_row_count.sql`)

```sql
SELECT
  COUNT(*) AS row_count,
  SUM(CASE WHEN y IS TRUE THEN 1 ELSE 0 END) AS positives,
  SUM(CASE WHEN y IS FALSE THEN 1 ELSE 0 END) AS negatives
FROM `uci-bank-marketing-ml-lab.bank_data.uci_bank_marketing`;
```

**Result:**

* Row count: 41,188
* Positives: 4,640
* Negatives: 36,548

---

### 2. Schema Validation (`verify_schema.sql`)

```sql
SELECT column_name, data_type, is_nullable
FROM `uci-bank-marketing-ml-lab.bank_data.INFORMATION_SCHEMA.COLUMNS`
ORDER BY ordinal_position;
```

**Result:**

* 16 columns detected
* Data types inferred correctly (e.g., INT64 for age, STRING for job)

---

### 3. Data Profiling (`basic_data_profiling.sql`)

```sql
WITH basics AS (
  SELECT
    COUNT(DISTINCT job) AS jobs,
    COUNT(DISTINCT marital) AS maritals,
    COUNT(DISTINCT education) AS educations,
    MIN(age) AS min_age, MAX(age) AS max_age,
    MIN(duration) AS min_dur, MAX(duration) AS max_dur,
    MIN(`emp var rate`) AS min_emp_var_rate, MAX(`emp var rate`) AS max_emp_var_rate
  FROM `uci-bank-marketing-ml-lab.bank_data.uci_bank_marketing`
)
SELECT * FROM basics;
```

**Result Highlights:**

* 12 unique job categories
* Age range: 17–98
* Duration range: 0–4918 seconds

---

## **Verification Evidence**

| **Screenshot File**              | **Description**                         |
| -------------------------------- | --------------------------------------- |
| `Bucket creation (`uci-bank-ml-bucket`).jpg` | Bucket creation (`uci-bank-ml-bucket`)  |
| `Uploaded files under `bank-additional/`.jpg` | Uploaded files under `bank-additional/` |
| `Cloud Shell `gsutil` verification .jpg` | Cloud Shell `gsutil` verification       |
| `Row count and imbalance query output.jpg` | Row count and imbalance query output    |
| `Schema verification results  .jpg` | Schema verification results             |
| `Data profiling output.jpg` | Data profiling output                   |
| `BigQuery connection summary .jpg` | BigQuery connection summary             |

---

## **Notebook Outputs**

| **Notebook Section** | **Purpose**                | **Action** |
| -------------------- | -------------------------- | ---------- |
| Config and Imports   | Setup project and clients  | Run        |
| Verify GCS Files     | List uploaded files        | Run        |
| Verify Dataset       | Check if dataset exists    | Run        |
| Verify Table         | Confirm table registration | Run        |
| Skip Load/Creation   | Avoid duplication          | Skipped    |

---

## **Reflection**

* Cloud Storage serves as the **landing zone** for raw or intermediate datasets.
* BigQuery functions as the **analytical layer** for querying, validation, and downstream ML input preparation.
* The notebook provides an auditable verification trail for the setup, ensuring future reproducibility and pipeline scalability.
* This setup forms the foundation for subsequent analytics, feature engineering, and Vertex AI workflows.

---
