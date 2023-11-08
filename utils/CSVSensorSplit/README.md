## CSV sensor splitter

This utility script splits a large sensor `.csv` file efficiently into chuncks of user-defined lines. This should be done to enable parallel stream of sensors

Alternatively, we can also use https://csvkit.readthedocs.io/en/latest/  for splitting the files


#### requirements

* python3
* dask

#### usage

* run split.py using python.
* arguments: 
* 
  - location of file
  - number of rows
  - number of threads used
  - output directory where the split sensor files will be present.
   
   
example:
```bash
$python split.py --numrows 5000000 --numthreads 4 --input_file KPI_CELL_day_all.csv --output_dir test
```