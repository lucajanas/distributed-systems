import warnings
warnings.filterwarnings('ignore')

import sys

print(sys.executable)

import os
os.environ["PYSPARK_PYTHON"] = sys.executable

import pyspark
from pyspark.sql import SparkSession

conf = pyspark.SparkConf().setMaster('spark://localhost:7077')
spark = SparkSession \
    .builder \
    .appName("Python") \
    .getOrCreate()

print('Submitted application!')

import pandas as pd

path = "C:\\Users\\Luca\\PycharmProjects\\distributed-systems\\load_simulation_data\\ts_data_1.csv"
df_pd = pd.read_csv(path)

print("Read csv via pandas")

print(df_pd.head())

sparkDF = spark.createDataFrame(df_pd)
print("Converted pandas DataFrame to spark DataFrame")
sparkDF.show()

df = spark.read.format("csv") \
    .option('header', True) \
    .option('multiLine', True) \
    .load(path)

print("Read csv directly via spark")

df.show()

print("Read data")
