import warnings
import sys
import os
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *

warnings.filterwarnings('ignore')
os.environ["PYSPARK_PYTHON"] = sys.executable

def connect():
    conf = pyspark.SparkConf().setMaster('spark://localhost:7077')
    spark = SparkSession \
        .builder \
        .appName("Python") \
        .getOrCreate()

    print('Submitted application!')
    return spark

def extract_data(path, sparkSession, number_of_files=6):

    # Creates Empty RDD
    emp_RDD = sparkSession.sparkContext.emptyRDD()
    columns = StructType([StructField('datetime', DateType(), False),
                           StructField('pulse', FloatType(), False),
                           StructField('category', StringType(), False),
                           StructField('ts_number', StringType(), False)])

    df = sparkSession.createDataFrame(data=emp_RDD, schema=columns)

    for i in range(1, number_of_files + 1):

        path_data = path + fr"/ts_data_block_{i}.csv"  # Change Datafile name if necessary

        df_temp = sparkSession.read.format("csv") \
            .option('header', True) \
            .option('multiLine', True) \
            .option('inferSchema', True) \
            .load(path_data)

        df = df.union(df_temp)

    # option('inferSchema', True): detects the correct format else every column is declined as string
    return df

