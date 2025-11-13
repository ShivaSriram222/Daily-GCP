# Exercise 5– Model Training with TFX Trainer

This exercise uses a custom `trainer_module.py` to train a binary classifier on the transformed dataset.

## Steps Completed

### **1. Built trainer_module.py**
- Implemented:
  - Input function reading transformed TFRecords
  - DNN classifier using Keras
  - End-to-end model training using tf.data
  - Serving function using Transform Graph
- Exported SavedModel with `serving_default` signature.

### **2. Ran TFX Trainer**
- Used ExampleGen + Transform outputs
- Produces artifacts:
  - Trained model
  - ModelRun metadata


