"""
Simple way to split csv file data using dask.
"""
from concurrent.futures import ThreadPoolExecutor
import math
import sys
import time
import argparse
import dask
import dask.dataframe as dd
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_rows', help='number of rows')
    parser.add_argument('--num_partitions', help='number of partitions')
    parser.add_argument('--num_threads', default=2, help='number of concurrent threads')
    parser.add_argument('--input_file',help='input file name')
    parser.add_argument('--output_dir',help='output directory')
    args = parser.parse_args()
    if (args.num_rows is not None) and (args.num_partitions is not None):
        print("Both number of rows and partitions are provided, but only 1 is accepted")
        sys.exit(0)
    if (args.num_rows is  None) and (args.num_partitions is  None):
        print("Either the number of rows or partitions must be provided")
        sys.exit(0)
        
    MODE_ROW=True
    if args.num_rows is not None:
        num_rows = int(args.num_rows)
    if args.num_partitions is not None:
        num_partitions=int(args.num_partitions)
        MODE_ROW=False
    # Dask configuration
    num_threads= int(args.num_threads)
    from dask.distributed import Client
    client = Client()
    dask.config.set(scheduler='threads')
    pool = ThreadPoolExecutor(num_threads)
    dask.config.set(pool=pool)

    start_time =time.time()
    df = dd.read_csv(args.input_file)
    TIME_FOR_SIZE =0
    if MODE_ROW:
        df_size =df.shape[0].compute()
        TIME_FOR_SIZE =time.time() - start_time
        num_partitions =math.ceil(df_size/num_rows)

    df_partitions=df.repartition(npartitions=num_partitions)
    outname = f"{args.output_dir}/data_*.csv"
    df_partitions.to_csv(outname,index=False)
    #df_partitions.compute()
    total_time =time.time() - start_time
    print(f'File is partitioned into {num_partitions} subfiles')
    print(f'Total time: {total_time} seconds, with {TIME_FOR_SIZE} seconds for determing size')
    