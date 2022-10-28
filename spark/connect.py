import warnings

warnings.filterwarnings('ignore')

import pyspark
from pyspark.sql import SparkSession

#import os
#print(os.getcwd())

conf = pyspark.SparkConf().setMaster('spark://172.18.0.22:7077')
#conf = pyspark.SparkConf().setMaster('spark://localhost:7077')

spark = SparkSession \
    .builder.config(conf=conf) \
    .appName("Python") \
    .getOrCreate()

#print(spark.sparkContext.getConf().getAll())

print('Submitted application!')

import pandas as pd

path = "file:///mnt/c/Users/Luca/PycharmProjects/distributed-systems/load_simulation_data/ts_data_block_1.csv"
path_pd = "/mnt/c/Users/Luca/PycharmProjects/distributed-systems/load_simulation_data/ts_data_block_1.csv"
# path_con = "file:///tmp/ts_data_1.csv"
#df_pd = pd.read_csv(path_pd)

path_win = "C:\\Users\\Luca\\PycharmProjects\\distributed-systems\\load_simulation_data\\ts_data_block_1.csv"

print("Read csv via pandas")

#print(df_pd.head())

#sparkDF = spark.createDataFrame(df_pd)
#print("Converted pandas DataFrame to spark DataFrame")
#sparkDF.show()

path_con = "file:///home/jovyan/work/ts_data_block_1.csv"

df = spark.read.format("csv") \
    .option('header', True) \
    .option('multiLine', True) \
    .load("file:////tmp/ts_data_1.csv")

print("Read csv directly via spark")

df.show()

print("Read data")
