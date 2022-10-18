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

# path = "C:\\Users\\Luca\\PycharmProjects\\distributed-systems\\load_simulation_data\\ts_data_1.csv"
path = r"/Users/kevin/Desktop/distributed-systems_copy/load_simulation_data/ts_data_1.csv"

df_pd = pd.read_csv(path)

print("Read csv via pandas")

print(df_pd.head())

sparkDF = spark.createDataFrame(df_pd)
print("Converted pandas DataFrame to spark DataFrame")
sparkDF.show()


# Read csv as spark.sql.dataframe.DataFrame format directly using Spark
df = spark.read.format("csv") \
    .option('header', True) \
    .option('multiLine', True) \
    .option('inferSchema', True) \
    .load(path)

    # option('inferSchema', True): detects the correct format else every column is declined as string

print("Read csv directly via spark")

df.show()

# Applying ML Classification on time series data

print("Groupby data and apply statistics on the column 'pulse'")
import pyspark.sql.functions as F

def groupby_describe(df, groupby_col, stat_col):
    out = df.groupby(groupby_col).agg(
        # F.count(stat_col).alias("count"),
        F.mean(stat_col).alias("mean"),
        F.stddev(stat_col).alias("std"),
        F.min(stat_col).alias("min"),
        F.expr(f"percentile({stat_col}, array(0.25))")[0].alias("low_quart"),
        F.expr(f"percentile({stat_col}, array(0.5))")[0].alias("median"),
        F.expr(f"percentile({stat_col}, array(0.75))")[0].alias("up_quart"),
        F.max(stat_col).alias("max"),
    )
    return out

df_stats = groupby_describe(df, ['ts_number', 'category'], 'pulse')
df_stats.show()


## Feature Engineering (encoding column "category")
print('Encoded category')
from pyspark.ml.feature import VectorAssembler, StringIndexer

catEncoder = StringIndexer(inputCol='category', outputCol='Target').fit(df_stats)
df_stats = catEncoder.transform(df_stats)
df_stats.show()

## Feature Selection
print('Features to vector')
required_features = ['mean', 'std', 'min', 'low_quart', 'median', 'up_quart', 'max', 'Target']
vec_assembler = VectorAssembler(inputCols=required_features, outputCol='features')
df_stats_vec = vec_assembler.transform(df_stats)
df_stats_vec.show()


print("Split Training and Test")
train_df, test_df = df_stats_vec.randomSplit([0.8, 0.2], seed=9)

print("Number of train dataset:")
print(train_df.count())
print("Number of test  dataset:")
print(test_df.count())

## Using Logistic Regression as Classification Model

print('Targetdata vs. predicted Data')

from pyspark.ml.classification import LogisticRegression

lr = LogisticRegression(featuresCol='features', labelCol='Target')
lr_model = lr.fit(train_df)

y_pred = lr_model.transform(test_df)
y_pred.select('Target', 'prediction').show()

## Model Evaluation
# Check for prediction Accuracy
print('Prediction Accuracy:')
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

multi_evaluator = MulticlassClassificationEvaluator(labelCol='Target', metricName='accuracy')
print(multi_evaluator.evaluate(y_pred))
