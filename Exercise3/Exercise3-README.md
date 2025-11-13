# Exercise 3 – Data Ingestion & Validation (TFX ExampleGen + StatisticsGen + SchemaGen + ExampleValidator)

This exercise focuses on ingesting raw CSV data and validating it using TFX components.

## Steps Completed

### **1. ExampleGen**
- Ingested raw CSV dataset.
- Generated `examples/` artifact with Train / Eval splits.

### **2. StatisticsGen**
- Computed descriptive statistics on training + eval data.
- Produced `stats/` artifact for visualization in TFMA / Facets.

### **3. SchemaGen**
- Auto-generated data schema from statistics.
- Verified feature types and distributions.

### **4. ExampleValidator**
- Checked raw data for anomalies:
  - Missing values
  - Type mismatches
  - Out-of-vocabulary values
  - Skew / drift detection

