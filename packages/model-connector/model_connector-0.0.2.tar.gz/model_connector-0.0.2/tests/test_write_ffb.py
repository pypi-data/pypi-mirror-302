import os
from typing import Union

import numpy as np
import pandas as pd
import pytest
from pytest import fixture

from model_connector.write_ffb import write_ffb
from model_connector.common import STRING_ENCODING, NULL_DOUBLE, NULL_FLOAT, NULL_INT

@fixture
def temp_file():
    """Return the path to a temporary file. Delete it on completion."""
    fname = "tests/test_data/temp.bin"
    dcb_name = os.path.splitext(fname)[0] + ".dcb"
    yield fname

    # Delete the file
    os.remove(fname)
    os.remove(dcb_name)

def read_binary(fname: str, dtype: Union[type, str]):
    with open(fname, "rb") as f:
        return np.fromfile(f, dtype=dtype)

# Test writing an integer 64 column
def test_write_integer64(temp_file):
    test_arr = [1, 2, 3]
    test_type = np.int64
    
    df = pd.DataFrame({"fld": test_arr})
    df['fld'] = df['fld'].astype(test_type)
    write_ffb(df, temp_file)

    # Read the file
    data = read_binary(temp_file, np.int32) #TC only supports 32 bit integers, so values are downcast

    assert np.array_equal(data, test_arr)
    
# Test writing an integer 32 column
def test_write_integer32(temp_file):
    test_arr = [1, 2, 3]
    test_type = np.int32

    df = pd.DataFrame({"fld": test_arr})
    df['fld'] = df['fld'].astype(test_type)
    write_ffb(df, temp_file)

    # Read the file
    data = read_binary(temp_file, test_type)

    assert np.array_equal(data, test_arr)

# Test writing an integer 16 column
def test_write_integer16(temp_file):
    test_arr = [1, 2, 3]
    test_type = np.int16

    df = pd.DataFrame({"fld": test_arr})
    df['fld'] = df['fld'].astype(test_type)
    write_ffb(df, temp_file)

    # Read the file
    data = read_binary(temp_file, test_type)

    assert np.array_equal(data, test_arr)

# Test writing an integer 8 column (TC Tiny)
def test_write_integer8(temp_file):
    test_arr = [1, 2, 3]
    test_type = np.uint8

    df = pd.DataFrame({"fld": test_arr})
    df['fld'] = df['fld'].astype(test_type)
    write_ffb(df, temp_file)

    # Read the file
    data = read_binary(temp_file, test_type)

    assert np.array_equal(data, test_arr)

# Test writing a float 64 (TC=Double) column
def test_write_float64(temp_file):
    test_arr = [1.1, 2.2, 3.3]
    test_type = np.float64
    df = pd.DataFrame({"fld": test_arr})
    df['fld'] = df['fld'].astype(test_type)
    write_ffb(df, temp_file)

    # Read the file
    data = read_binary(temp_file, test_type)

    assert np.array_equal(data, test_arr)

# Test writing a float 32 (TC=Float) column
def test_write_float32(temp_file):
    test_arr = [1.1, 2.2, 3.3]
    test_type = np.float32
    df = pd.DataFrame({"fld": test_arr})
    df['fld'] = df['fld'].astype(test_type)
    write_ffb(df, temp_file)

    # Read the file
    data = read_binary(temp_file, test_type)

    assert np.array_equal(data, np.array(test_arr).astype(test_type))

# Test writing a string column
def test_write_string(temp_file):
    test_arr = ["a", "b", "c"]
    test_type = np.dtype('S1')
    df = pd.DataFrame({"fld": test_arr})
    df['fld'] = df['fld']
    write_ffb(df, temp_file)

    # Read the file
    data = read_binary(temp_file, "S1")

    assert np.array_equal(data, [bytes(x, STRING_ENCODING) for x in test_arr])

# Test writing a date column
def test_write_date(temp_file):
    test_arr = [pd.Timestamp("2021-01-01"), pd.Timestamp("2021-01-02"), pd.Timestamp("2021-01-03")]
    test_type = np.int32
    df = pd.DataFrame({"fld": test_arr})
    write_ffb(df, temp_file)

    # Read the file
    data = read_binary(temp_file, test_type)

    assert np.array_equal(data, [20210101, 20210102, 20210103])

# Test writing a time column
def test_write_time(temp_file):
    test_arr = [pd.Timestamp(6000, unit="ms"), pd.Timestamp(7000, unit="ms"), pd.Timestamp(8000, unit="ms")]
    test_type = np.int32
    df = pd.DataFrame({"fld": test_arr})
    write_ffb(df, temp_file)

    # Read the file
    data = read_binary(temp_file, test_type)

    assert np.array_equal(data, [6000, 7000, 8000])

# Test writing a datetime column
def test_write_datetime(temp_file):
    test_arr = [pd.Timestamp("2021-01-01 00:00:05"), pd.Timestamp("2021-01-02 00:00:06"), pd.Timestamp("2021-01-03 00:00:07")]
    test_type = np.int32
    df = pd.DataFrame({"fld": test_arr})
    write_ffb(df, temp_file)

    # Read the file
    data = np.array(read_binary(temp_file, "<i4,<i4")).tolist()

    #assert np.array_equal(data, [(20210101, 5000), (20210102, 6000), (20210103, 7000)])
    assert np.array_equal(data, [(20210101, 5000), (20210102, 6000), (20210103, 7000)])
    #assert np.array_equal(data[0], [20210101, 5000])

def test_write_float64_null(temp_file):
    test_arr = [1.1, 2.2, None]
    test_type = np.float64
    df = pd.DataFrame({"fld": test_arr})
    df['fld'] = df['fld'].astype(test_type)
    write_ffb(df, temp_file)

    # Read the file
    data = read_binary(temp_file, test_type)

    assert np.array_equal(data, [1.1, 2.2, NULL_DOUBLE])

def test_write_float32_null(temp_file):
    test_arr = [1.1, 2.2, None]
    test_type = np.float32
    df = pd.DataFrame({"fld": test_arr})
    df['fld'] = df['fld'].astype(test_type)
    write_ffb(df, temp_file)

    # Read the file
    data = read_binary(temp_file, test_type)

    test_arr = [np.float32(test_arr[0]), 
                np.float32(test_arr[1]),
                np.float32(NULL_FLOAT)]
    
    assert np.array_equal(data, test_arr)

def test_write_string_null(temp_file):
    test_arr = ["aaa", "bbb", None]
    test_type = np.dtype('S1')
    df = pd.DataFrame({"fld": test_arr})
    df['fld'] = df['fld']
    write_ffb(df, temp_file)

    # Read the file
    data = read_binary(temp_file, "S3")

    test_arr = [bytes(test_arr[0], STRING_ENCODING), 
                bytes(test_arr[1], STRING_ENCODING),
                b"   "] #null is written as all spaces

    assert np.array_equal(data, test_arr)

def test_write_date_null(temp_file):
    test_arr = [pd.Timestamp("2021-01-01"), pd.Timestamp("2021-01-02"), None]
    test_type = np.int32
    df = pd.DataFrame({"fld": test_arr})
    write_ffb(df, temp_file)

    # Read the file
    data = read_binary(temp_file, test_type)

    assert np.array_equal(data, [20210101, 20210102, NULL_INT])

def test_write_time_null(temp_file):
    test_arr = [pd.Timestamp(6000, unit="ms"), pd.Timestamp(7000, unit="ms"), None]
    test_type = np.int32
    df = pd.DataFrame({"fld": test_arr})
    write_ffb(df, temp_file)

    # Read the file
    data = read_binary(temp_file, test_type)

    assert np.array_equal(data, [6000, 7000, NULL_INT])

def test_write_datetime_null(temp_file):
    test_arr = [pd.Timestamp("2021-01-01 00:00:05"), pd.Timestamp("2021-01-02 00:00:06"), None]
    test_type = np.int32
    df = pd.DataFrame({"fld": test_arr})
    write_ffb(df, temp_file)

    # Read the file
    data = np.array(read_binary(temp_file, "<i4,<i4")).tolist()

    assert np.array_equal(data, [(20210101, 5000), (20210102, 6000), (NULL_INT, NULL_INT)])