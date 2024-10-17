# model-connector: Library for accessing travel model data

## Installation:

Install using pip

```pip install model-connector```


## Example Usage

Reading from a TransCAD binary file

```python
import model_connector as mc

# Read a TransCAD fixed format binary file into a dataframe, 
# retaining null values
df = mc.read_csv("myfile.bin")

# Read a TransCAD fixed format binary file into a dataframe, 
# converting null values to zeros
dfz = mc.read_csv("myfile.bin", null_to_zero=True)
```

Writing to a TransCAD binary file
```python
import model_connector as mc
import pandas as pd

df = pd.DataFrame({"ID":[1,2,3], 
                   "RealField":[1.1, 2.2, 3.3, ],
                   "IntField":[1, 2, 3],
                   "DateField":[20210101, 20210115, 20210130],
                   "DateTimeField":[pd.Timestamp("2021-01-01 00:00:05"),
                                    pd.Timestamp("2021-01-15 00:10:05"),
                                    pd.Timestamp("2021-01-30 00:20:05")]})

mc.write_ffb(df, "sample_output.bin")
```

