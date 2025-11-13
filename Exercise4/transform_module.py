import tensorflow as tf
import tensorflow_transform as tft

NUMERIC_FEATURES = [
    "age",
    "campaign",
    "pdays",
    "previous",
    "emp_var_rate",
    "cons_price_idx",
    "cons_conf_idx",
    "euribor3m",
    "nr_employed",
    "duration",
]

CATEGORICAL_FEATURES = [
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "month",
    "day_of_week",
    "poutcome",
]

LABEL_KEY = "y"  


def _make_label(x):
    """Handle both string and numeric label representations."""
    if x.dtype == tf.string:
        # UCI style: "yes" / "no"
        return tf.cast(tf.equal(x, b"yes"), tf.int64)
    else:
        # Already numeric (0/1 or similar) -> just cast
        return tf.cast(x, tf.int64)


def preprocessing_fn(inputs):
    outputs = {}

    # Numeric features -> z-score normalized
    for key in NUMERIC_FEATURES:
        if key in inputs:
            outputs[key + "_z"] = tft.scale_to_z_score(
                tf.cast(inputs[key], tf.float32)
            )

    # Categorical features -> vocab IDs
    for key in CATEGORICAL_FEATURES:
        if key in inputs:
            outputs[key + "_id"] = tft.compute_and_apply_vocabulary(
                inputs[key],
                top_k=100,
                num_oov_buckets=1,
            )

    # Label -> 0/1 int64
    if LABEL_KEY in inputs:
        outputs[LABEL_KEY] = _make_label(inputs[LABEL_KEY])

    return outputs
