# TFX End-to-End ML Pipeline – Bank Marketing Classifier

This repository contains **four standalone exercises**, each representing a major stage of an MLOps pipeline implemented with **TensorFlow Extended (TFX)** on **Google Cloud Platform**.

##  Pipeline Overview

| Stage | Folder | Description |
|------|--------|-------------|
| 1)  Ingestion & Validation | `1_ingestion_validation/` | Load raw CSV, compute statistics, generate schema, detect anomalies |
| 2️) Feature Engineering | `2_feature_engineering/` | Apply TensorFlow Transform, generate Transform Graph + transformed dataset |
| 3️) Trainer | `3_trainer/` | Build training dataset, custom Trainer module, Train+Export SavedModel |
| 4️) Evaluator & Pusher | `4_evaluator_pusher/` | Evaluate the model using TFMA and push if blessed |

## Technologies Used

- **TFX**
- **TensorFlow Transform**
- **TensorFlow Model Analysis**
- **Keras 3**
- **Apache Beam**
- **GCP AI Notebook**
- **GCP Cloud Storage**

## GCP Proof
Screenshots included in each exercise folder show execution inside Google Cloud AI Notebook + output artifacts stored in Cloud Storage.

##  Goal
To demonstrate deep understanding of MLOps concepts including:
- reproducible pipelines  
- data validation  
- transform graph reuse  
- training with user-defined modules  
- model evaluation & controlled promotion  
- serving-ready SavedModels  
