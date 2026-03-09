#!/usr/bin/env python3
"""
Mock Data Generator for Machine Learning Testing

Generates train data and predict result data for binary classification,
multiclass classification, and regression tasks. Supports Federated Learning
scenarios with guest/host CSV split.
"""

import argparse
import os
import sys
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd


def set_random_seed(seed: Optional[int]) -> None:
    """Set random seed for reproducibility."""
    if seed is not None:
        np.random.seed(seed)


def generate_features(
    n_samples: int,
    n_features: int,
    seed: Optional[int] = None
) -> pd.DataFrame:
    """Generate mixed numeric features (int and float columns)."""
    if seed is not None:
        np.random.seed(seed)

    features = {}

    # Mix of int and float features (roughly 50/50 split)
    n_int = n_features // 2
    n_float = n_features - n_int

    # Integer features
    for i in range(n_int):
        col_name = f"feature_{i}"
        # Random range for integers: -1000 to 1000
        features[col_name] = np.random.randint(-1000, 1001, size=n_samples)

    # Float features
    for i in range(n_float):
        col_name = f"feature_{n_int + i}"
        # Random range for floats: -100.0 to 100.0
        features[col_name] = np.random.uniform(-100.0, 100.0, size=n_samples)

    df = pd.DataFrame(features)
    df.insert(0, "id", range(n_samples))

    return df


def generate_target(
    task_type: str,
    n_samples: int,
    n_classes: int = 2,
    class_imbalance_ratio: float = 0.5,
    noise_level: float = 0.1,
    features: Optional[pd.DataFrame] = None,
    seed: Optional[int] = None
) -> np.ndarray:
    """
    Generate target variable y based on features with configurable noise and imbalance.

    Args:
        task_type: 'binary', 'multiclass', or 'regression'
        n_samples: Number of samples
        n_classes: Number of classes for classification
        class_imbalance_ratio: Ratio for majority class (e.g., 0.9 for 90:10)
        noise_level: Amount of noise to add (0.0 to 1.0)
        features: Feature DataFrame to base y on (optional)
        seed: Random seed

    Returns:
        Array of target values
    """
    if seed is not None:
        np.random.seed(seed)

    if features is not None and len(features.columns) > 1:
        # Use actual feature columns to generate y (excluding id)
        feature_cols = [c for c in features.columns if c != "id"]
        X = features[feature_cols].values

        # Create a linear combination of features
        weights = np.random.randn(X.shape[1])
        linear_combo = X @ weights

        # Add non-linearity for more realistic relationships
        non_linear = np.sin(linear_combo * 0.1) + 0.5 * (linear_combo ** 2) / (linear_combo.max() ** 2 + 1e-8)

        # Add noise
        noise = np.random.normal(0, noise_level, n_samples)
        signal = non_linear + noise
    else:
        # Fallback: random signal
        signal = np.random.randn(n_samples)

    if task_type == "binary":
        # Convert signal to binary with class imbalance
        threshold = np.percentile(signal, (1 - class_imbalance_ratio) * 100)
        y = (signal > threshold).astype(int)

    elif task_type == "multiclass":
        # Convert signal to multiclass with class imbalance
        # Use weighted quantiles to create imbalance
        thresholds = []
        cumulative = 0.0

        # Create imbalanced class distribution
        class_weights = np.array([class_imbalance_ratio ** i for i in range(n_classes)])
        class_weights = class_weights / class_weights.sum()

        for w in class_weights[:-1]:
            cumulative += w
            thresholds.append(np.percentile(signal, cumulative * 100))

        y = np.zeros(n_samples, dtype=int)
        for i, thresh in enumerate(thresholds):
            y[signal > thresh] = i + 1

    elif task_type == "regression":
        # Scale signal for regression
        y = signal * 100 + np.random.normal(0, noise_level * 50, n_samples)

    else:
        raise ValueError(f"Unknown task type: {task_type}")

    return y


def inject_edge_cases(
    df: pd.DataFrame,
    edge_case_ratio: float = 0.1,
    config: Optional[Dict] = None
) -> pd.DataFrame:
    """
    Inject comprehensive edge cases into the dataframe.

    Edge cases include:
    - Class imbalance (handled in target generation)
    - Extreme outliers (values 5-10x outside normal range)
    - Boundary values (min/max of data types)
    - Correlated features (Pearson > 0.9)
    - Near-zero variance (>95% identical values)
    - Scale differences (mix of small and large ranges)
    - Skewed distributions (long-tail)
    - Multicollinearity (high inter-correlation)
    - Feature interactions (non-linear relationships)
    - Near-duplicates (99% correlated)
    - Sparse features (>80% zero values)
    """
    if config is None:
        config = {}

    df = df.copy()
    feature_cols = [c for c in df.columns if c != "id" and c != "y"]
    n_samples = len(df)
    n_edge_cases = int(n_samples * edge_case_ratio)

    if n_edge_cases == 0 or len(feature_cols) == 0:
        return df

    # Convert feature columns to float64 to allow mixed type assignments
    for col in feature_cols:
        df[col] = df[col].astype(np.float64)

    # Select random rows for edge case injection
    edge_indices = np.random.choice(df.index, size=min(n_edge_cases, len(df)), replace=False)

    # 1. Extreme outliers: 5-10x outside normal range
    outlier_cols = np.random.choice(feature_cols, size=min(2, len(feature_cols)), replace=False)
    for col in outlier_cols:
        col_mean = df[col].mean()
        col_std = df[col].std()
        outlier_indices = np.random.choice(edge_indices, size=len(edge_indices) // 3, replace=False)
        # Values 5-10 standard deviations away
        direction = np.random.choice([-1, 1], size=len(outlier_indices))
        multiplier = np.random.uniform(5, 10, size=len(outlier_indices))
        df.loc[outlier_indices, col] = col_mean + direction * multiplier * col_std

    # 2. Boundary values: INT_MAX, FLOAT_MAX, 0, 1
    boundary_cols = np.random.choice(feature_cols, size=min(2, len(feature_cols)), replace=False)
    for i, col in enumerate(boundary_cols):
        boundary_indices = np.random.choice(edge_indices, size=len(edge_indices) // 4, replace=False)
        if df[col].dtype in [np.int64, np.int32]:
            # For integer columns, use INT_MAX, INT_MIN, 0, or 1
            boundary_values = np.random.choice([0, 1, np.iinfo(np.int32).max, np.iinfo(np.int32).min], size=len(boundary_indices))
        else:
            # For float columns, use float max/min, 0.0, 1.0
            boundary_values = np.random.choice([0.0, 1.0, np.finfo(np.float32).max, np.finfo(np.float32).min], size=len(boundary_indices))
        df.loc[boundary_indices, col] = boundary_values

    # 3. Correlated features: Create features with Pearson > 0.9
    if len(feature_cols) >= 2:
        corr_col_base = feature_cols[0]
        corr_col_new = f"feature_corr_{np.random.randint(1000)}"
        # Create highly correlated feature (r > 0.9)
        noise_factor = 0.1  # Small noise for high correlation
        df[corr_col_new] = df[corr_col_base] + np.random.normal(0, df[corr_col_base].std() * noise_factor, n_samples)
        feature_cols.append(corr_col_new)

    # 4. Near-zero variance: >95% identical values
    if len(feature_cols) > 0:
        nvz_col = f"feature_nzv_{np.random.randint(1000)}"
        constant_value = np.random.choice([0, 1, 100])
        df[nvz_col] = constant_value
        # Vary only 5% of values
        vary_indices = np.random.choice(df.index, size=int(n_samples * 0.05), replace=False)
        df.loc[vary_indices, nvz_col] = constant_value + np.random.randn(len(vary_indices))
        feature_cols.append(nvz_col)

    # 5. Scale differences: Mix of small (0-1) and large (0-1e6) ranges
    if len(feature_cols) > 0:
        # Small scale feature
        small_col = f"feature_small_{np.random.randint(1000)}"
        df[small_col] = np.random.uniform(0, 1, n_samples)
        feature_cols.append(small_col)

        # Large scale feature
        large_col = f"feature_large_{np.random.randint(1000)}"
        df[large_col] = np.random.uniform(0, 1e6, n_samples)
        feature_cols.append(large_col)

    # 6. Skewed distributions: Long-tail (log-normal, exponential)
    if len(feature_cols) > 0:
        skew_col = f"feature_skew_{np.random.randint(1000)}"
        # Log-normal distribution (long right tail)
        df[skew_col] = np.random.lognormal(0, 2, n_samples)
        feature_cols.append(skew_col)

    # 7. Multicollinearity: Multiple features with high inter-correlation
    if len(feature_cols) >= 2:
        base_col = feature_cols[0]
        for i in range(2):  # Create 2 multicollinear features
            multi_col = f"feature_multi_{i}_{np.random.randint(1000)}"
            # Create feature with high correlation to base
            df[multi_col] = df[base_col] * (0.8 + 0.2 * np.random.randn(n_samples)) + np.random.randn(n_samples) * 0.1
            feature_cols.append(multi_col)

    # 8. Feature interactions: Non-linear relationships
    if len(feature_cols) >= 2:
        interact_col = f"feature_interact_{np.random.randint(1000)}"
        # Product of two features
        col_a, col_b = feature_cols[0], feature_cols[1]
        df[interact_col] = df[col_a] * df[col_b] / 1000  # Scale down
        feature_cols.append(interact_col)

    # 9. Near-duplicates: Features 99% correlated
    if len(feature_cols) > 0:
        dup_col = f"feature_dup_{np.random.randint(1000)}"
        base = feature_cols[0]
        # Almost exact copy with tiny noise
        df[dup_col] = df[base] + np.random.normal(0, 0.01, n_samples)
        feature_cols.append(dup_col)

    # 10. Sparse features: >80% zero values
    if len(feature_cols) > 0:
        sparse_col = f"feature_sparse_{np.random.randint(1000)}"
        df[sparse_col] = 0
        # Only 20% non-zero
        non_zero_indices = np.random.choice(df.index, size=int(n_samples * 0.2), replace=False)
        df.loc[non_zero_indices, sparse_col] = np.random.uniform(1, 100, size=len(non_zero_indices))
        feature_cols.append(sparse_col)

    return df


def generate_train_data(
    task_type: str,
    n_samples: int,
    n_features: int,
    output_dir: str,
    edge_case_ratio: float = 0.1,
    n_classes: int = 2,
    class_imbalance_ratio: float = 0.5,
    noise_level: float = 0.1,
    seed: Optional[int] = None
) -> Tuple[str, str]:
    """
    Generate train data split into guest and host CSVs for Federated Learning.

    Returns:
        Tuple of (guest_file_path, host_file_path)
    """
    set_random_seed(seed)

    # Generate features
    df = generate_features(n_samples, n_features, seed)

    # Generate target based on features
    y = generate_target(
        task_type=task_type,
        n_samples=n_samples,
        n_classes=n_classes,
        class_imbalance_ratio=class_imbalance_ratio,
        noise_level=noise_level,
        features=df,
        seed=seed
    )
    df["y"] = y

    # Inject edge cases
    df = inject_edge_cases(df, edge_case_ratio)

    # Split for Federated Learning
    # Guest has y + some features, Host has features only (no y)
    # For simplicity, we put all features in both but y only in guest
    guest_df = df.copy()
    host_df = df.drop(columns=["y"])

    # Save files
    os.makedirs(output_dir, exist_ok=True)

    guest_file = os.path.join(output_dir, f"{task_type}_train_guest.csv")
    host_file = os.path.join(output_dir, f"{task_type}_train_host.csv")

    guest_df.to_csv(guest_file, index=False)
    host_df.to_csv(host_file, index=False)

    return guest_file, host_file


def generate_predict_data(
    task_type: str,
    n_samples: int,
    n_classes: int = 2,
    class_imbalance_ratio: float = 0.5,
    noise_level: float = 0.1,
    seed: Optional[int] = None
) -> pd.DataFrame:
    """
    Generate predict result data with predictions, scores, and true values.

    Returns:
        DataFrame with predict result columns
    """
    set_random_seed(seed)

    df = pd.DataFrame({"id": range(n_samples)})

    # Generate true target
    y_true = generate_target(
        task_type=task_type,
        n_samples=n_samples,
        n_classes=n_classes,
        class_imbalance_ratio=class_imbalance_ratio,
        noise_level=noise_level,
        seed=seed
    )
    df["true_result"] = y_true

    if task_type == "binary":
        # Generate prediction scores (probabilities)
        # Simulate model predictions that are somewhat correlated with true labels
        # but with some errors
        noise = np.random.normal(0, 0.2, n_samples)
        true_probs = y_true.astype(float) + noise
        true_probs = np.clip(true_probs, 0, 1)  # Clip to [0, 1]

        # Add some randomness to simulate imperfect model
        predict_score = 0.7 * true_probs + 0.3 * np.random.beta(2, 2, n_samples)
        df["predict_score"] = np.clip(predict_score, 0, 1)

        # Predicted class based on threshold 0.5
        df["predict_result"] = (df["predict_score"] > 0.5).astype(int)

    elif task_type == "multiclass":
        # Generate class probabilities that sum to 1
        # Create probabilities that favor the true class but with uncertainty
        prob_matrix = np.zeros((n_samples, n_classes))

        for i in range(n_samples):
            true_class = int(y_true[i])
            # Higher probability for true class
            probs = np.random.dirichlet([0.5] * n_classes)
            probs[true_class] += np.random.uniform(0.3, 0.7)
            probs = probs / probs.sum()  # Renormalize
            prob_matrix[i] = probs

        # Add label columns
        for c in range(n_classes):
            df[f"label_{c}"] = prob_matrix[:, c]

        # Predicted class is argmax
        df["predict_result"] = prob_matrix.argmax(axis=1)

        # Predict score is max probability
        df["predict_score"] = prob_matrix.max(axis=1)

    elif task_type == "regression":
        # For regression: predict_result is the prediction, predict_score is confidence
        # Predictions are close to true values with some error
        error = np.random.normal(0, noise_level * 50, n_samples)
        df["predict_result"] = y_true + error

        # Confidence score based on error magnitude (higher error = lower confidence)
        error_magnitude = np.abs(error)
        max_error = error_magnitude.max() + 1e-8
        df["predict_score"] = 1 - (error_magnitude / max_error)

    else:
        raise ValueError(f"Unknown task type: {task_type}")

    # Reorder columns
    if task_type == "multiclass":
        label_cols = [f"label_{c}" for c in range(n_classes)]
        df = df[["id", "predict_result", "predict_score", "true_result"] + label_cols]
    else:
        df = df[["id", "predict_result", "predict_score", "true_result"]]

    return df


def save_predict_output(
    df: pd.DataFrame,
    task_type: str,
    output_dir: str
) -> str:
    """Save predict result to CSV."""
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{task_type}_predict_result.csv")
    df.to_csv(output_file, index=False)
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Generate mock data for machine learning testing"
    )

    parser.add_argument(
        "--data-type",
        choices=["train", "predict"],
        required=True,
        help="Type of data to generate: 'train' (guest/host CSVs) or 'predict' (predict result)"
    )

    parser.add_argument(
        "--task-type",
        choices=["binary", "multiclass", "regression"],
        required=True,
        help="ML task type"
    )

    parser.add_argument(
        "--num-samples",
        type=int,
        default=1000,
        help="Number of samples to generate (default: 1000)"
    )

    parser.add_argument(
        "--num-features",
        type=int,
        default=10,
        help="Number of features for train data (default: 10)"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="./output",
        help="Output directory (default: ./output)"
    )

    parser.add_argument(
        "--edge-case-ratio",
        type=float,
        default=0.1,
        help="Ratio of samples with edge cases injected (default: 0.1)"
    )

    parser.add_argument(
        "--num-classes",
        type=int,
        default=3,
        help="Number of classes for multiclass classification (default: 3)"
    )

    parser.add_argument(
        "--class-imbalance-ratio",
        type=float,
        default=0.5,
        help="Class imbalance ratio, e.g., 0.9 for 90:10 (default: 0.5)"
    )

    parser.add_argument(
        "--noise-level",
        type=float,
        default=0.1,
        help="Noise level for target generation, 0.0 to 1.0 (default: 0.1)"
    )

    parser.add_argument(
        "--random-seed",
        type=int,
        default=None,
        help="Random seed for reproducibility (default: None)"
    )

    args = parser.parse_args()

    print(f"Generating {args.data_type} data for {args.task_type} task...")
    print(f"  Samples: {args.num_samples}")
    if args.data_type == "train":
        print(f"  Features: {args.num_features}")
    print(f"  Output dir: {args.output_dir}")
    if args.random_seed is not None:
        print(f"  Random seed: {args.random_seed}")

    if args.data_type == "train":
        guest_file, host_file = generate_train_data(
            task_type=args.task_type,
            n_samples=args.num_samples,
            n_features=args.num_features,
            output_dir=args.output_dir,
            edge_case_ratio=args.edge_case_ratio,
            n_classes=args.num_classes,
            class_imbalance_ratio=args.class_imbalance_ratio,
            noise_level=args.noise_level,
            seed=args.random_seed
        )
        print(f"\nGenerated train files:")
        print(f"  Guest (with y): {guest_file}")
        print(f"  Host (no y):    {host_file}")

    else:  # predict
        predict_df = generate_predict_data(
            task_type=args.task_type,
            n_samples=args.num_samples,
            n_classes=args.num_classes,
            class_imbalance_ratio=args.class_imbalance_ratio,
            noise_level=args.noise_level,
            seed=args.random_seed
        )
        output_file = save_predict_output(predict_df, args.task_type, args.output_dir)
        print(f"\nGenerated predict result file:")
        print(f"  {output_file}")

    print("\nDone!")


if __name__ == "__main__":
    main()
