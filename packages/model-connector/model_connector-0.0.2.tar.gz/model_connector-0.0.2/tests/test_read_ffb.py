import numpy as np
import pandas as pd
import pytest
from pytest import fixture

from model_connector.read_ffb import read_ffb, FileFormatError


@fixture
def simple_df():
    test_file = "tests/test_data/simple.bin"
    return read_ffb(test_file)


@fixture
def simple_null_df():
    test_file = "tests/test_data/simple_withnull.bin"
    return read_ffb(test_file)

@fixture
def simple_null_to_zero_df():
    test_file = "tests/test_data/simple_withnull.bin"
    return read_ffb(test_file, null_to_zero=True)


@fixture
def simple_deleted_df():
    test_file = "tests/test_data/simple_deleted.bin"
    return read_ffb(test_file)


# ---- Test each field type ----
def test_read_simple(simple_df):
    assert simple_df.shape == (2, 9)


def test_integer(simple_df):
    assert simple_df["fld_integer"].dtype == "int32"
    assert simple_df["fld_integer"].sum() == 3


def test_real(simple_df):
    assert simple_df["fld_real"].dtype == "float64"
    assert (
        simple_df["fld_real"].sum() == 1.1 + 2.2
    )  # can't use 3.3 directly because of floating point precision


def test_string(simple_df):
    assert simple_df["fld_string"].dtype == "object"
    assert simple_df["fld_string"].sum() == "onetwo"


def test_short(simple_df):
    assert simple_df["fld_short"].dtype == "int16"
    assert simple_df["fld_short"].sum() == 3


def test_tiny(simple_df):
    assert simple_df["fld_tiny"].dtype == "uint8"
    assert simple_df["fld_tiny"].sum() == 3


def test_float(simple_df):
    assert simple_df["fld_float"].dtype == "float32"
    assert simple_df["fld_float"].sum() == np.float32(1.1) + np.float32(2.2)


def test_date(simple_df):
    assert simple_df["fld_date"].dtype == "datetime64[ns]"
    assert simple_df["fld_date"][0] == pd.to_datetime("2001-01-15")
    assert simple_df["fld_date"][1] == pd.to_datetime("2002-02-25")


def test_time(simple_df):
    assert simple_df["fld_time"].dtype == "datetime64[ns]"
    assert simple_df["fld_time"][0] == pd.to_datetime("1970-01-01 13:01:01")
    assert simple_df["fld_time"][1] == pd.to_datetime("1970-01-01 14:02:02")


def test_datetime(simple_df):
    assert simple_df["fld_datetime"].dtype == "datetime64[ns]"
    assert simple_df["fld_datetime"][0] == pd.to_datetime("2001-01-01 13:01:01")
    assert simple_df["fld_datetime"][1] == pd.to_datetime("2002-02-02 14:02:02")


# ---- Test null values ----
def test_null_read(simple_null_df):
    assert simple_null_df.shape == (3, 9)


def test_null_integer(simple_null_df):
    assert simple_null_df["fld_integer"].dtype == "float64"
    assert np.isnan(simple_null_df["fld_integer"][2])


def test_null_real(simple_null_df):
    assert simple_null_df["fld_real"].dtype == "float64"
    assert np.isnan(simple_null_df["fld_real"][2])


def test_null_string(simple_null_df):
    assert simple_null_df["fld_string"].dtype == "object"
    assert pd.isnull(simple_null_df["fld_string"][2])


def test_null_short(simple_null_df):
    assert simple_null_df["fld_short"].dtype == "float64"
    assert np.isnan(simple_null_df["fld_short"][2])


def test_null_tiny(simple_null_df):
    assert simple_null_df["fld_tiny"].dtype == "float64"
    assert np.isnan(simple_null_df["fld_tiny"][2])


def test_null_float(simple_null_df):
    assert simple_null_df["fld_float"].dtype == "float32"
    assert np.isnan(simple_null_df["fld_float"][2])


def test_null_date(simple_null_df):
    assert simple_null_df["fld_date"].dtype == "datetime64[ns]"
    assert pd.isnull(simple_null_df["fld_date"][2])


def test_null_time(simple_null_df):
    assert simple_null_df["fld_time"].dtype == "datetime64[ns]"
    assert pd.isnull(simple_null_df["fld_time"][2])


def test_null_datetime(simple_null_df):
    assert simple_null_df["fld_datetime"].dtype == "datetime64[ns]"
    assert pd.isnull(simple_null_df["fld_datetime"][2])


# ---- Test null values with null read as zeros ----
def test_null_to_zero_read(simple_null_to_zero_df):
    assert simple_null_to_zero_df.shape == (3, 9)

def test_null_to_zero_integer(simple_null_to_zero_df):
    assert simple_null_to_zero_df["fld_integer"].dtype == "int32"
    assert simple_null_to_zero_df["fld_integer"][2] == 0

def test_null_to_zero_real(simple_null_to_zero_df):
    assert simple_null_to_zero_df["fld_real"].dtype == "float64"
    assert simple_null_to_zero_df["fld_real"][2] == 0.0

def test_null_to_zero_string(simple_null_to_zero_df):
    assert simple_null_to_zero_df["fld_string"].dtype == "object"
    assert simple_null_to_zero_df["fld_string"][2] == ""

def test_null_to_zero_short(simple_null_to_zero_df):
    assert simple_null_to_zero_df["fld_short"].dtype == "int16"
    assert simple_null_to_zero_df["fld_short"][2] == 0

def test_null_to_zero_tiny(simple_null_to_zero_df):
    assert simple_null_to_zero_df["fld_tiny"].dtype == "uint8"
    assert simple_null_to_zero_df["fld_tiny"][2] == 0

def test_null_to_zero_float(simple_null_to_zero_df):
    assert simple_null_to_zero_df["fld_float"].dtype == "float32"
    assert simple_null_to_zero_df["fld_float"][2] == 0.0

def test_null_to_zero_date(simple_null_to_zero_df):
    assert simple_null_to_zero_df["fld_date"].dtype == "datetime64[ns]"
    assert pd.isnull(simple_null_to_zero_df["fld_datetime"][2]) #datetime is not converted to 0

def test_null_to_zero_time(simple_null_to_zero_df):
    assert simple_null_to_zero_df["fld_time"].dtype == "datetime64[ns]"
    assert pd.isnull(simple_null_to_zero_df["fld_datetime"][2]) #datetime is not converted to 0

def test_null_to_zero_datetime(simple_null_to_zero_df):
    assert simple_null_to_zero_df["fld_datetime"].dtype == "datetime64[ns]"
    assert pd.isnull(simple_null_to_zero_df["fld_datetime"][2]) #datetime is not converted to 0


# ---- Test deleted records ----


def test_deleted_read(simple_deleted_df):
    assert simple_deleted_df.shape == (1, 9)


def test_deleted_integer(simple_deleted_df):
    assert simple_deleted_df["fld_integer"].dtype == "int32"
    assert simple_deleted_df["fld_integer"].sum() == 1

# Not re-testing all fields for deleted records,
#   just a subset to confirm that the deleted record was skipped


def test_deleted_all():
    test_file = "tests/test_data/all_deleted.bin"
    df = read_ffb(test_file)
    assert df.shape == (0, 9)


# ---- Test exceptions ----


def test_bad_file():
    with pytest.raises(FileNotFoundError):
        read_ffb("tests/test_data/does_not_exist.bin")


def test_bad_dictionary():
    with pytest.raises(FileNotFoundError):
        read_ffb("tests/test_data/bad_dict.bin")


def test_bad_record_length():
    with pytest.raises(FileFormatError):
        read_ffb("tests/test_data/bad_record_length.bin")


def test_bad_dictionary_line1():
    with pytest.raises(FileFormatError):
        read_ffb("tests/test_data/bad_dict_line1.bin")
