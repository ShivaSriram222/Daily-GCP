# Exercise 4 – Feature Engineering with TensorFlow Transform (TFX Transform)

This exercise implements scalable preprocessing using `tft` with a custom `transform_module.py`.

## Steps Completed

### **1. Built transform_module.py**
- Applied normalization for numeric columns.
- Built vocabulary for categoricals.
- Handled missing values / outliers.
- Exported a Transform Graph that can be reused during training + serving.

### **2. Ran the TFX Transform Component**
- Loaded raw examples.
- Applied preprocessing in Beam.
- Generated:
  - `transform_graph/`
  - `transformed_examples/` dataset
