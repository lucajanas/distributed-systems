import sys

print(sys.executable)

import pyspark
from pyspark.sql import SparkSession

conf = pyspark.SparkConf().setMaster('spark://localhost:7077')
spark = SparkSession \
    .builder.config(conf=conf) \
    .appName("Python") \
    .getOrCreate()

# sc = pyspark.SparkContext(conf=conf)
# rdd = spark.sparkContext.textFile("file:///tmp/ts_data_1.csv")
# df = rdd.toDF()
# from pyspark import SparkFiles

# df = spark.sparkContext.textFile(SparkFiles.get('/tmp/ts_data_1.csv'))
# df.show()

print('Submitted application!')

import pandas as pd

path = "C:\\Users\\Luca\\PycharmProjects\\distributed-systems\\load_simulation_data\\ts_data_1.csv"
df_pd = pd.read_csv(path)

print(df_pd.head())

sparkDF = spark.createDataFrame(df_pd)
sparkDF.show()

df = spark.read.format("csv") \
    .option('header', True) \
    .option('multiLine', True) \
    .load(path)
# .load(path)

# df.show()

print("Read data")
