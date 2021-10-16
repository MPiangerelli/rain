import pytest

from simple_repo import (
    PandasColumnSelector,
    PandasPivot,
    PandasRenameColumn,
    SklearnLinearSVC,
    SimpleKMeans,
    SparkCSVLoader,
    SparkModelLoader,
    SaveModel,
    SaveDataset,
    SparkColumnSelector,
    SparkSplitDataset,
    Tokenizer,
    HashingTF,
    LogisticRegression,
    SparkPipelineNode,
)
from simple_repo.exception import ParameterNotFound
from simple_repo.simple_io.pandas_io import (
    PandasInputNode,
    PandasOutputNode,
    PandasCSVLoader,
    PandasCSVWriter,
)
from simple_repo.simple_pandas.node_structure import PandasNode
from simple_repo.simple_sklearn.node_structure import (
    SklearnClassifier,
    SklearnEstimator,
    SklearnClusterer,
    SklearnNode,
)

# TODO per come è impostato ora questo test non servono più i singoli test sui metodi nei moduli test degli engine. Detronizzarli!

# for each class write the expected list of inputs, output and methods (if present) respectively
from simple_repo.simple_spark.node_structure import (
    SparkInputNode,
    SparkOutputNode,
    SparkNode,
    Transformer,
    Estimator,
)

classes = [
    # Sklearn Nodes
    (SklearnNode, [], [], []),
    (SklearnEstimator, ["fit_dataset"], ["fitted_model"], ["fit"]),
    (
        SklearnClassifier,
        ["fit_dataset", "predict_dataset", "score_dataset"],
        ["fitted_model", "predictions", "scores"],
        ["fit", "predict", "score"],
    ),
    (
        SklearnClusterer,
        ["fit_dataset", "predict_dataset", "score_dataset", "transform_dataset"],
        ["fitted_model", "predictions", "scores", "transformed_dataset"],
        ["fit", "predict", "score", "transform"],
    ),
    (
        SimpleKMeans,
        ["fit_dataset", "predict_dataset", "score_dataset", "transform_dataset"],
        ["fitted_model", "predictions", "scores", "transformed_dataset"],
        ["fit", "predict", "score", "transform"],
    ),
    (
        SklearnLinearSVC,
        ["fit_dataset", "predict_dataset", "score_dataset"],
        ["fitted_model", "predictions", "scores"],
        ["fit", "predict", "score"],
    ),  # Pandas Nodes
    (PandasInputNode, None, ["dataset"], None),
    (PandasCSVLoader, None, ["dataset"], None),
    (PandasOutputNode, ["dataset"], None, None),
    (PandasCSVWriter, ["dataset"], None, None),
    (PandasNode, ["dataset"], ["dataset"], None),
    (PandasColumnSelector, ["dataset"], ["dataset"], None),
    (PandasPivot, ["dataset"], ["dataset"], None),
    (PandasRenameColumn, ["dataset"], ["dataset"], None),  # Spark Nodes
    (SparkInputNode, None, [], None),
    (SparkCSVLoader, None, ["dataset"], None),
    (SparkModelLoader, None, ["model"], None),
    (SparkOutputNode, [], None, None),
    (SaveModel, ["model"], None, None),
    (SaveDataset, ["dataset"], None, None),
    (SparkNode, ["dataset"], [], None),
    (Transformer, ["dataset"], ["dataset"], None),
    (SparkColumnSelector, ["dataset"], ["dataset"], None),
    (
        SparkSplitDataset,
        ["dataset"],
        ["dataset", "train_dataset", "test_dataset"],
        None,
    ),
    (Tokenizer, ["dataset"], ["dataset"], None),
    (HashingTF, ["dataset"], ["dataset"], None),
    (Estimator, ["dataset"], ["model"], None),
    (LogisticRegression, ["dataset"], ["model"], None),
    (SparkPipelineNode, ["dataset"], ["model"], None),
]


@pytest.mark.parametrize("class_, in_vars, out_vars, methods_vars", classes)
def test_class_integrity(class_, in_vars, out_vars, methods_vars):
    input_string = "_input_vars"
    output_string = "_output_vars"
    methods_string = "_methods"

    if in_vars is None:
        assert not hasattr(class_, input_string)
    else:
        assert set(in_vars) == set(class_._input_vars.keys())

    if out_vars is None:
        assert not hasattr(class_, output_string)
    else:
        assert set(out_vars) == set(class_._output_vars.keys())

    if methods_vars is None:
        assert not hasattr(class_, methods_string)
    else:
        assert set(methods_vars) == set(class_._methods.keys())


def check_param_not_found(class_, **kwargs):
    """Checks whether the class raises a TypeError exception when instantiating,
    meaning that an invalid argument has been passed."""
    with pytest.raises(TypeError):
        class_("s1", **kwargs)
