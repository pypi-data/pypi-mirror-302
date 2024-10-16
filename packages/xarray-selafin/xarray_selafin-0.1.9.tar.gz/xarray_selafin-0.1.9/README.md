# xarray backend for Selafin formats

Supports lazy loading by default.

## Dev guide

To have the backend working in xarray, follow these steps:

```
pip install xarray-selafin
```

## Read Selafin

```python
import xarray as xr
ds = xr.open_dataset("tests/data/r3d_tidal_flats.slf", engine="selafin")
ds = xr.open_dataset("tests/data/r3d_tidal_flats.slf", lang="fr", engine="selafin")  # if variables are in French
```

```
<xarray.Dataset>
Dimensions:  (time: 17, node: 648, plan: 21)
Coordinates:
    x        (node) float32 ...
    y        (node) float32 ...
  * time     (time) datetime64[ns] 1900-01-01 ... 1900-01-02T20:26:40
Dimensions without coordinates: node, plan
Data variables:
    Z        (time, node, plan) <class 'numpy.float64'> ...
    U        (time, node, plan) <class 'numpy.float64'> ...
    V        (time, node, plan) <class 'numpy.float64'> ...
    W        (time, node, plan) <class 'numpy.float64'> ...
    MUD      (time, node, plan) <class 'numpy.float64'> ...
Attributes:
    title:       Sloped flume Rouse profile test
    language:    en
    float_size:  4
    endian:      >
    params:      (1, 0, 0, 0, 0, 0, 21, 5544, 0, 1)
    ipobo:       [   1  264  263 ... 5411 5412 5413]
    ikle2:       [[155 153 156]\n [310 307 305]\n [308 310 305]\n ...\n [537 ...
    ikle3:       [[  155   153   156   803   801   804]\n [  310   307   305 ...
    variables:   {'Z': ('ELEVATION Z', 'M'), 'U': ('VELOCITY U', 'M/S'), 'V':...
    date_start:  (1900, 1, 1, 0, 0, 0)
```

## Indexing

```python
ds_last = ds.isel(time=-1)  # last frame
```

## Manipulate variables

```python
ds = ds.assign(UTIMES100=lambda x: x.U * 100)  # Add a new variable
# ds.attrs["variables"]["UTIMES100"] = ("UTIMES100", "My/Unit")  # To provide variable name and unit (optional)
ds.drop_vars(["W"])  # Remove variable `VELOCITY W`
```

## Write Selafin

```python
ds.selafin.write("output_file.slf")
```

## DataSet content

### Dimensions
* time
* node
* plan (only in 3D)
 
### Coordinates

| Coordinate | Description            |
|------------|------------------------|
| x          | East mesh coordinates  |
| y          | North mesh coordinates |
| time       | Datetime serie         |

### Attributes

All attributes are optional except `ikle2`:

| Attribute  | Description                                                             | Default value            | 
|------------|-------------------------------------------------------------------------|--------------------------|
| title      | Serafin title                                                           | "" (empty string)        |
| language   | Language for variable detection                                         | "en"                     |
| float_size | Float size                                                              | 4 (single precision)     |
| endian     | File endianness                                                         | ">"                      |
| params     | Table of integer parameters                                             | (can be rebuilt)         |
| ikle2      | Connectivity table in 2D (1-indexed)                                    | -                        |
| ikle3      | Connectivity table in 3D (1-indexed, only in 3D, optional)              | (can be rebuilt from 2D) |
| variables  | Dictionary with variable names and units (key is variable abbreviation) | -                        |
| date_start | Starting date with integers (year to seconds)                           | (from first time serie)  |
