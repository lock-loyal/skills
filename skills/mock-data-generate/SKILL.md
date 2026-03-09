---
name: mock-data-generate
description: Generate mock data for machine learning testing including binary/multiclass classification and regression. Creates train data with edge cases and predict results with Federated Learning split (guest/host CSVs). Supports reproducible generation with random seed. Use when user needs test data for ML models, federated learning scenarios, or edge case testing.
---

# Mock Data Generate

## Overview

This skill generates realistic mock data for machine learning testing, specifically designed for Federated Learning scenarios. It supports three task types (binary classification, multiclass classification, regression) and creates both train data (split into guest/host CSVs) and predict result data with realistic prediction scores.

Key capabilities:
- **Task types**: Binary, multiclass, and regression
- **Federated Learning ready**: Train data splits into guest (with y) and host (without y) CSVs
- **Realistic targets**: Y values generated as a function of features with configurable noise
- **Edge cases**: Comprehensive injection of challenging data scenarios
- **Reproducible**: Random seed support for consistent results

## Quick Start

### Binary Classification Train Data

```bash
python scripts/generate_mock_data.py \
    --data-type train \
    --task-type binary \
    --num-samples 1000 \
    --num-features 10 \
    --random-seed 42
```

Generates:
- `binary_train_guest.csv` - id, y, feature_0, feature_1, ...
- `binary_train_host.csv` - id, feature_0, feature_1, ... (no y)

### Multiclass Classification Predict Results

```bash
python scripts/generate_mock_data.py \
    --data-type predict \
    --task-type multiclass \
    --num-samples 500 \
    --num-classes 4 \
    --random-seed 42
```

Generates:
- `multiclass_predict_result.csv` - id, predict_result, predict_score, true_result, label_0, label_1, label_2, label_3

### Regression Train Data

```bash
python scripts/generate_mock_data.py \
    --data-type train \
    --task-type regression \
    --num-samples 2000 \
    --num-features 20
```

Generates:
- `regression_train_guest.csv` - id, y (continuous), 20 features
- `regression_train_host.csv` - id, 20 features (no y)

## Workflow

### Step 1: Determine Task Type

Identify the machine learning task:
- **Binary**: Two classes (0/1), e.g., fraud detection, churn prediction
- **Multiclass**: Multiple classes (0, 1, 2, ...), e.g., image classification, sentiment categories
- **Regression**: Continuous values, e.g., price prediction, demand forecasting

### Step 2: Choose Data Type

- **Train data** (`--data-type train`): Use when you need training datasets
  - Creates guest/host split for Federated Learning
  - Features are a mix of integers and floats
  - Target variable y is generated from features with configurable noise

- **Predict results** (`--data-type predict`): Use when you need prediction output format
  - Simulates model predictions with scores and confidence
  - Includes true labels for evaluation

### Step 3: Set Parameters

Key parameters:
| Parameter | Description | Default |
|-----------|-------------|---------|
| `--num-samples` | Number of rows to generate | 1000 |
| `--num-features` | Number of feature columns (train only) | 10 |
| `--num-classes` | Classes for multiclass (train/predict) | 3 |
| `--edge-case-ratio` | Portion of data with edge cases | 0.1 |
| `--class-imbalance-ratio` | Imbalance ratio (e.g., 0.9 for 90:10) | 0.5 |
| `--noise-level` | Noise in target generation (0.0-1.0) | 0.1 |
| `--random-seed` | For reproducibility | None |

### Step 4: Run and Verify

Execute the script and verify output files.

## Task Types

### Binary Classification

Target `y` is 0 or 1, generated based on feature relationships with configurable class imbalance.

**Train output columns:**
- `id`: Unique identifier
- `y`: Binary target (0 or 1)
- `feature_*`: Mixed int/float features

**Predict output columns:**
- `id`: Unique identifier
- `predict_result`: Predicted class (0 or 1)
- `predict_score`: Prediction probability (0.0-1.0)
- `true_result`: Actual class (0 or 1)

### Multiclass Classification

Target `y` is 0, 1, 2, ..., n-1 with configurable class imbalance.

**Train output columns:**
- `id`: Unique identifier
- `y`: Multiclass target (0 to n_classes-1)
- `feature_*`: Mixed int/float features

**Predict output columns:**
- `id`: Unique identifier
- `predict_result`: Predicted class (0 to n_classes-1)
- `predict_score`: Max probability across classes (0.0-1.0)
- `true_result`: Actual class (0 to n_classes-1)
- `label_0` to `label_{n-1}`: Probability for each class (sum to ~1.0)

### Regression

Target `y` is continuous float, generated from features with noise.

**Train output columns:**
- `id`: Unique identifier
- `y`: Continuous target value (float)
- `feature_*`: Mixed int/float features

**Predict output columns:**
- `id`: Unique identifier
- `predict_result`: Predicted continuous value
- `predict_score`: Confidence score (0.0-1.0, higher = more confident)
- `true_result`: Actual continuous value

## Edge Cases Covered

The generator injects comprehensive edge cases into a portion of the data (controlled by `--edge-case-ratio`):

### 1. Class Imbalance
Skewed class distribution controlled by `--class-imbalance-ratio`:
- 0.5 = balanced (default)
- 0.9 = 90:10 ratio for binary
- Higher values for multiclass create exponential decay

### 2. Extreme Outliers
Values 5-10x outside the normal range (5-10 standard deviations from mean).

### 3. Boundary Values
Min/max values of data types:
- Integers: INT_MAX, INT_MIN, 0, 1
- Floats: FLOAT_MAX, FLOAT_MIN, 0.0, 1.0

### 4. Correlated Features
Pearson correlation > 0.9 between feature pairs, created by adding small noise to base features.

### 5. Near-Zero Variance
Features with >95% identical values (e.g., all zeros except 5% varied).

### 6. Scale Differences
Mix of ranges in the same dataset:
- Small: 0-1
- Normal: -1000 to 1000
- Large: 0 to 1,000,000

### 7. Skewed Distributions
Long-tail distributions using log-normal, creating right-skewed data.

### 8. Multicollinearity
Multiple features with high inter-correlation (>0.8), challenging for linear models.

### 9. Feature Interactions
Non-linear relationships (e.g., product of two features).

### 10. Near-Duplicates
Features 99% correlated with tiny random noise added.

### 11. Sparse Features
Features with >80% zero values (e.g., 20% non-zero).

## Output Format

### Train Data (Federated Learning Split)

**Guest CSV** (`{task_type}_train_guest.csv`):
```
id,y,feature_0,feature_1,feature_2,...
0,1,42,-12.5,890,...
1,0,-15,34.2,-234,...
...
```

**Host CSV** (`{task_type}_train_host.csv`):
```
id,feature_0,feature_1,feature_2,...
0,42,-12.5,890,...
1,-15,34.2,-234,...
...
```

### Predict Result CSV

**Binary/Regression** (`{task_type}_predict_result.csv`):
```
id,predict_result,predict_score,true_result
0,1,0.87,1
1,0,0.23,0
...
```

**Multiclass** (`{task_type}_predict_result.csv`):
```
id,predict_result,predict_score,true_result,label_0,label_1,label_2,label_3
0,2,0.65,2,0.15,0.20,0.65,0.00
1,0,0.78,0,0.78,0.12,0.08,0.02
...
```

## Script Reference

### Full Parameter List

```
--data-type {train,predict}
    Type of data to generate

--task-type {binary,multiclass,regression}
    ML task type

--num-samples N
    Number of samples to generate (default: 1000)

--num-features N
    Number of features for train data (default: 10)

--output-dir PATH
    Output directory (default: ./output)

--edge-case-ratio FLOAT
    Ratio of samples with edge cases (default: 0.1)

--num-classes N
    Number of classes for multiclass (default: 3)

--class-imbalance-ratio FLOAT
    Class imbalance ratio, e.g., 0.9 for 90:10 (default: 0.5)

--noise-level FLOAT
    Noise level for target generation, 0.0 to 1.0 (default: 0.1)

--random-seed N
    Random seed for reproducibility (default: None)
```

### Advanced Examples

**Severe class imbalance (95:5):**
```bash
python scripts/generate_mock_data.py \
    --data-type train \
    --task-type binary \
    --num-samples 10000 \
    --class-imbalance-ratio 0.95 \
    --random-seed 42
```

**High noise regression:**
```bash
python scripts/generate_mock_data.py \
    --data-type train \
    --task-type regression \
    --num-samples 5000 \
    --num-features 50 \
    --noise-level 0.5 \
    --edge-case-ratio 0.2
```

**Multiclass with 10 classes:**
```bash
python scripts/generate_mock_data.py \
    --data-type predict \
    --task-type multiclass \
    --num-samples 1000 \
    --num-classes 10 \
    --class-imbalance-ratio 0.3
```

## Target Generation Details

The target variable `y` is generated as a function of the features to ensure realistic relationships:

1. **Linear combination**: Features are combined with random weights
2. **Non-linearity**: Sine and quadratic transformations applied
3. **Noise**: Gaussian noise added (controlled by `--noise-level`)
4. **Discretization**: For classification, thresholds create classes with configurable imbalance

This approach ensures:
- Features are predictive of the target
- Relationships are non-trivial (not purely linear)
- Noise simulates real-world uncertainty
- Class imbalance is controllable

## Reproducibility

To generate identical datasets across runs, use `--random-seed`:

```bash
# First run
python scripts/generate_mock_data.py --data-type train --task-type binary --random-seed 42

# Second run - identical output
python scripts/generate_mock_data.py --data-type train --task-type binary --random-seed 42
```

Without a seed, each run produces different random data.
