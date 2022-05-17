from typing import Literal

# https://colab.research.google.com/drive/1hIYF5DVMy-dnAL_llRDwZ85wf8UzZ5B8?hl=ja#scrollTo=jeMUaZ9pkZt0


def create_dummy_model(typ="keras"):
    import keras

    model = keras.Sequential(
        [
            keras.layers.Flatten(
                input_shape=(28, 28)
            ),  # 画像を（28×28ピクセルの）2次元配列から、28×28＝784ピクセルの、1次元配列に変換
            keras.layers.Dense(
                128, activation="relu"
            ),  # 密結合あるいは全結合されたニューロンの層  128個のノード（あるはニューロン）があります
            keras.layers.Dense(
                10, activation="softmax"
            ),  # 2番めの層は、10ノードのsoftmax層です。この層は、合計が1になる10個の確率の配列を返します。それぞれのノードは、今見ている画像が10個のクラスのひとつひとつに属する確率を出力します。
        ]
    )
    return model


def get_model_json(path):
    # model = create_dummy_model()
    # model.to_json()
    return {
        "keras_version": "2.8.0",
        "backend": "tensorflow",
        "class_name": "Sequential",
        "config": {
            "name": "sequential",
            "layers": [
                {
                    "class_name": "InputLayer",
                    "config": {
                        "batch_input_shape": [None, 28, 28],
                        "dtype": "float32",
                        "sparse": False,
                        "ragged": False,
                        "name": "flatten_input",
                    },
                },
                {
                    "class_name": "Flatten",
                    "config": {
                        "name": "flatten",
                        "trainable": True,
                        "batch_input_shape": [None, 28, 28],
                        "dtype": "float32",
                        "data_format": "channels_last",
                    },
                },
                {
                    "class_name": "Dense",
                    "config": {
                        "name": "dense",
                        "trainable": True,
                        "dtype": "float32",
                        "units": 128,
                        "activation": "relu",
                        "use_bias": True,
                        "kernel_initializer": {
                            "class_name": "GlorotUniform",
                            "config": {"seed": None},
                        },
                        "bias_initializer": {"class_name": "Zeros", "config": {}},
                        "kernel_regularizer": None,
                        "bias_regularizer": None,
                        "activity_regularizer": None,
                        "kernel_constraint": None,
                        "bias_constraint": None,
                    },
                },
                {
                    "class_name": "Dense",
                    "config": {
                        "name": "dense_1",
                        "trainable": True,
                        "dtype": "float32",
                        "units": 10,
                        "activation": "softmax",
                        "use_bias": True,
                        "kernel_initializer": {
                            "class_name": "GlorotUniform",
                            "config": {"seed": None},
                        },
                        "bias_initializer": {"class_name": "Zeros", "config": {}},
                        "kernel_regularizer": None,
                        "bias_regularizer": None,
                        "activity_regularizer": None,
                        "kernel_constraint": None,
                        "bias_constraint": None,
                    },
                },
            ],
        },
    }


def get_model_weights(path, save_format: Literal["h5", "tf"] = "h5"):
    model = create_dummy_model()
    model.save_weights(path, save_format=save_format)
