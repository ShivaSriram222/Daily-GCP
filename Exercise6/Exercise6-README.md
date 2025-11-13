# Exercise 4 – Model Evaluation & Deployment (Evaluator + Pusher)

This exercise uses TFMA to evaluate the trained model and Pusher to export it for serving.

## Steps Completed

### **1. Built EvalConfig**
- Provided:
  - `label_key="y"`
  - `prediction_key="output_0"`
  - `signature_name="serving_default"`
- Enabled metrics:
  - AUC
  - Accuracy

### **2. Ran Evaluator**
- Compared Eval datasets against predictions.
- Produced model blessing artifact.

### **3. Ran Pusher**

