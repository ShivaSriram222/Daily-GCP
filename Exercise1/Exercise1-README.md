
# Day 1 — GCP Setup: Vertex AI, BigQuery & Cloud Storage Enablement  
**Project:** UCI Bank Marketing ML Lab  

---

## 1. Introduction

This first challenge establishes the foundation for the entire *UCI Bank Marketing Machine Learning Lab* series.  
The goal is to build a fully functional Google Cloud environment capable of supporting data analysis, model training, and deployment.

By the end of this stage, the cloud environment should be ready to:
- Run Vertex AI models  
- Query data in BigQuery  
- Store and retrieve large datasets using Cloud Storage  
- Authenticate securely via IAM service accounts  

This setup ensures a **production-ready foundation** before any data science or ML work begins.

---

## 2. Environment Summary

| Component | Details |
|------------|----------|
| **Project ID** | `uci-bank-marketing-ml-lab` |
| **Region** | `us-central1 (Iowa)` |
| **Billing** | Free Trial Account ($300 credit remaining) |
| **Service Account** | `bank-ml-runner@uci-bank-marketing-ml-lab.iam.gserviceaccount.com` |
| **Bucket Name** | `uci-bank-ml-bucket` |
| **Dataset** | UCI Bank Marketing Dataset |

---

## 3. Step-by-Step Implementation

### Step 1 — Project Creation and Billing

A new GCP project was created and linked to a free-trial billing account.  
This enables access to APIs, monitoring, and budgeting.

**Verification Screenshot:**  
![Billing Overview](Exercise1/billing_overview.jpg)

---

### Step 2 — API Enablement

The following core APIs were activated to support ML and data workflows.

| API | Service Name | Purpose | Status |
|------|---------------|----------|---------|
| Vertex AI | `aiplatform.googleapis.com` | Model training and prediction | Enabled |
| BigQuery | `bigquery.googleapis.com` | SQL-based data analytics | Enabled |
| Cloud Storage | `storage.googleapis.com` | Dataset storage and retrieval | Enabled |

**Screenshots:**  
- ![Vertex AI Enabled](images/Day1_GCPSetup/vertex_ai.png)  
- ![BigQuery Enabled](images/Day1_GCPSetup/bigquery_api.png)  
- ![Cloud Storage Enabled](images/Day1_GCPSetup/cloud_storage_api.png)  

**Command Used:**  
```bash
gcloud services list --enabled
````

![Enabled Services](images/Day1_GCPSetup/gcloud_enabled_services.png)

---

### Step 3 — Service Account and IAM Configuration

A dedicated service account named `bank-ml-runner` was created to isolate access credentials for ML workloads.
Instead of using default project credentials, this account ensures clear security boundaries and auditable permissions.

**Assigned Roles:**

| Role                    | Description                                |
| ----------------------- | ------------------------------------------ |
| `roles/aiplatform.user` | Enables Vertex AI model operations         |
| `roles/bigquery.user`   | Allows dataset queries                     |
| `roles/storage.admin`   | Grants dataset upload/download permissions |

**Verification Screenshots:**

* ![Service Account Created](images/Day1_GCPSetup/service_account_created.png)
* ![IAM Role Verification](images/Day1_GCPSetup/iam_roles_check.png)

**Command Verification:**

```bash
gcloud projects get-iam-policy uci-bank-marketing-ml-lab \
  --flatten="bindings[].members" \
  --format="table(bindings.role)" \
  --filter="bindings.members:bank-ml-runner"
```

Output:

```
ROLE: roles/aiplatform.user
ROLE: roles/bigquery.user
ROLE: roles/storage.admin
```

---

### Step 4 — Cloud Storage Setup

Created the bucket `uci-bank-ml-bucket` in region `us-central1` with **Standard** storage and **Uniform Access** permissions.

To organize the dataset, a folder named `bank-additional/` was created inside the bucket.
The dataset from the UCI repository was uploaded successfully.

| File Name                   | Type | Size   |
| --------------------------- | ---- | ------ |
| `bank-additional-full.csv`  | CSV  | 5.8 MB |
| `bank-additional.csv`       | CSV  | 584 KB |
| `bank-additional-names.txt` | TXT  | 5 KB   |

**Screenshot of Uploaded Files:**
![Dataset in Bucket](images/Day1_GCPSetup/dataset_uploaded.png)

---

### Step 5 — Verification and Validation

After configuration, the following checks confirmed the setup integrity:

1. Verified enabled APIs with `gcloud services list --enabled`
2. Checked IAM role bindings for `bank-ml-runner`
3. Validated dataset upload via the Cloud Console and `gsutil ls`

**Result:**
All services are active, roles correctly assigned, and data accessible.

---

## 4. Deliverables Checklist

| Deliverable                      | Description                                   | Status    |
| -------------------------------- | --------------------------------------------- | --------- |
| Project Created & Billing Linked | `uci-bank-marketing-ml-lab`                   | Completed |
| Core APIs Enabled                | Vertex AI, BigQuery, Cloud Storage            | Completed |
| IAM Roles Configured             | aiplatform.user, bigquery.user, storage.admin | Completed |
| Storage Bucket Setup             | `uci-bank-ml-bucket` created                  | Completed |
| Dataset Uploaded                 | All three UCI dataset files uploaded          | Completed |
| Environment Validated            | gcloud verification successful                | Completed |

---

## 5. Observations and Key Learnings

1. Learned how GCP projects organize resources under a clear hierarchy of project → service → IAM → billing.
2. Understood the importance of **service accounts** for authentication in production ML workflows.
3. Confirmed how enabling APIs like Vertex AI, BigQuery, and Cloud Storage lays the groundwork for scalable data pipelines.
4. Validated proper dataset organization inside buckets for easier BigQuery imports later.
5. Established the foundation for a reproducible and secure cloud ML environment.

---
