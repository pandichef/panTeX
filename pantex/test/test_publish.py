import os
import pickle
from pantex.publish import Manager
import pandas as pd
import pytest

test_directory = os.path.dirname(os.path.abspath(__file__))
test_context_dict = {
    "a": 1,
    "b": pd.DataFrame({"col1": [1, 2, 3], "col2": [2, 3, 4]}),
    "c": "foo",
}


def test_get_context_dict():
    m = Manager("my_template.md", {"a": 1, "b": 2})
    assert m.get_context()["a"] == 1
    assert m.get_context()["b"] == 2


def test_pickle_fixture():
    with open(f"{test_directory}./pickle_fixture.pkl", "rb") as fn:
        retrieved_context = pickle.loads(fn.read())
    assert test_context_dict["a"] == retrieved_context["a"]
    assert test_context_dict["c"] == retrieved_context["c"]
    assert list(test_context_dict["b"]["col1"]) == list(retrieved_context["b"]["col1"])
    assert list(test_context_dict["b"]["col2"]) == list(retrieved_context["b"]["col2"])


def test_save_context_dict():
    m = Manager(
        "my_template.md", f"{test_directory}/context.pkl"
    )  # saved as a pickle file by default
    result = m.save_context(test_context_dict)
    assert result == f"{test_directory}/context.pkl"
    with open(result, "rb") as fn:
        retrieved_context = pickle.loads(fn.read())
    assert test_context_dict["a"] == retrieved_context["a"]
    assert test_context_dict["c"] == retrieved_context["c"]
    assert list(test_context_dict["b"]["col1"]) == list(retrieved_context["b"]["col1"])
    assert list(test_context_dict["b"]["col2"]) == list(retrieved_context["b"]["col2"])


def test__render_pandas_dataframe():
    m = Manager(
        "my_template.md", f"{test_directory}/context.pkl"
    )  # saved as a pickle file by default
    rendered = m._render_pandas_dataframe(test_context_dict["b"], "Raw Data")
    assert "Table: Raw Data" in rendered
    assert "col1" in rendered
    assert "col2" in rendered


def test__render_pandas_dataframe_df_type():
    m = Manager(
        "my_template.md", f"{test_directory}/context.pkl"
    )  # saved as a pickle file by default
    with pytest.raises(AttributeError):
        rendered = m._render_pandas_dataframe("some_string", "Raw Data")


# def _render_matplotlib_figure  # todo
