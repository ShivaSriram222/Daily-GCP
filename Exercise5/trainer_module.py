import tensorflow as tf
import tensorflow_transform as tft

LABEL_KEY = "y"


def _get_feature_keys_from_schema(schema):
    """Collect all transformed feature names except the label."""
    feature_keys = []
    for feature in schema.feature:
        if feature.name == LABEL_KEY:
            continue
        feature_keys.append(feature.name)
    return feature_keys


def _make_file_list(file_input):
    """Normalize fn_args.train_files / eval_files to a flat list of files."""
    if isinstance(file_input, str):
        patterns = [file_input]
    else:
        patterns = list(file_input)

    files = []
    for p in patterns:
        files.extend(tf.io.gfile.glob(p))
    return files


def _input_fn(file_input, tf_transform_output, batch_size=128):
    """Builds an input_fn reading transformed TFRecords (supports GZIP)."""
    transformed_feature_spec = tf_transform_output.transformed_feature_spec()

    files = _make_file_list(file_input)
    if not files:
        raise ValueError(f"No TFRecord files found for pattern(s): {file_input}")

    # Detect compression (TFX often writes gzip-compressed TFRecords)
    compression_type = None
    if any(f.endswith(".gz") for f in files):
        compression_type = "GZIP"

    dataset = tf.data.TFRecordDataset(
        files,
        compression_type=compression_type
    )

    def _parse_fn(serialized_example):
        return tf.io.parse_single_example(serialized_example, transformed_feature_spec)

    dataset = dataset.map(_parse_fn, num_parallel_calls=tf.data.AUTOTUNE)

    def _split_features_label(example):
        label = example.pop(LABEL_KEY)
        label = tf.cast(label, tf.float32)
        if len(label.shape) == 0:
            label = tf.reshape(label, [1])
        return example, label

    dataset = dataset.map(_split_features_label,
                          num_parallel_calls=tf.data.AUTOTUNE)

    # Repeat so we always have enough batches for steps_per_epoch
    dataset = dataset.shuffle(10000).repeat().batch(batch_size).prefetch(tf.data.AUTOTUNE)
    return dataset


def _build_keras_model(feature_keys):
    """Simple DNN over concatenated transformed features."""
    inputs = {
        key: tf.keras.Input(shape=(1,), name=key, dtype=tf.float32)
        for key in feature_keys
    }

    x = tf.keras.layers.Concatenate()(list(inputs.values()))
    x = tf.keras.layers.Dense(64, activation="relu")(x)
    x = tf.keras.layers.Dense(32, activation="relu")(x)
    outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss="binary_crossentropy",
        metrics=[tf.keras.metrics.AUC(name="auc"), "accuracy"],
    )
    return model


class _ServingModule(tf.Module):
    """Wrapper module that holds both the model and the Transform layer."""

    def __init__(self, model, transform_layer, raw_feature_spec):
        super().__init__()
        # These are tracked resources/variables
        self.model = model
        self.transform_layer = transform_layer
        self.raw_feature_spec = raw_feature_spec

    @tf.function(
        input_signature=[
            tf.TensorSpec(shape=[None], dtype=tf.string, name="examples")
        ]
    )
    def serve_tf_examples_fn(self, serialized_tf_examples):
        """Serving fn: tf.Example -> transformed features -> model -> predictions."""
        # Parse raw features from tf.Example
        raw_features = tf.io.parse_example(serialized_tf_examples,
                                           self.raw_feature_spec)

        # Apply Transform graph
        transformed_features = self.transform_layer(raw_features)

        # Call the Keras model (expects transformed features dict)
        outputs = self.model(transformed_features)

        # TFMA & Pusher expect a dict of outputs
        return {"output_0": outputs}


def run_fn(fn_args):
    """TFX Trainer entrypoint."""
    # 1) Load transform output
    tf_transform_output = tft.TFTransformOutput(fn_args.transform_output)

    # 2) Figure out which transformed features to feed the model
    transformed_schema = tf_transform_output.transformed_metadata.schema
    feature_keys = _get_feature_keys_from_schema(transformed_schema)

    # 3) Build model
    model = _build_keras_model(feature_keys)

    # 4) Build datasets
    train_ds = _input_fn(fn_args.train_files, tf_transform_output, batch_size=128)
    eval_ds = _input_fn(fn_args.eval_files, tf_transform_output, batch_size=128)

    # 5) Train
    model.fit(
        train_ds,
        steps_per_epoch=fn_args.train_steps,
        validation_data=eval_ds,
        validation_steps=fn_args.eval_steps,
    )

    # 6) Prepare objects needed for serving
    transform_layer = tf_transform_output.transform_features_layer()
    raw_feature_spec = tf_transform_output.raw_feature_spec()

    # Remove the label from serving inputs (we don't send labels at serving time)
    if LABEL_KEY in raw_feature_spec:
        raw_feature_spec.pop(LABEL_KEY)

    # 7) Wrap into a tf.Module that tracks both model and transform layer
    serving_module = _ServingModule(
        model=model,
        transform_layer=transform_layer,
        raw_feature_spec=raw_feature_spec,
    )

    # 8) Export SavedModel with a tf.Example-based serving_default signature
    tf.saved_model.save(
        obj=serving_module,
        export_dir=fn_args.serving_model_dir,
        signatures={
            "serving_default": serving_module.serve_tf_examples_fn
        },
    )
