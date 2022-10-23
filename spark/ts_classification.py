from connect import connect, extract_data
import time
import pyspark.sql.functions as F
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

start_all = time.time()

# Get connection
spark = connect()
print("")
# Read Datafiles from connect.py module


print("Read csv directly via spark and union all datafiles into one PySpark Dataframe:")
start_0 = time.time()
df = extract_data(path=r"/Users/kevin/Desktop/Data Time Series Cross sectional",
                  sparkSession=spark,
                  number_of_files=6)
end_0 = time.time()
# Show Dataframe
df.show()
print(f'Elapsed time (minutes) for reading and union all datafiles: {(end_0-start_0)/60}')
print(f'Dataframe consists of {df.count()} rows.')
print("")


# Applying Machine Learning Classification Model on time series data.

## Feature Engineering

print("Group by time series data by ts_number and category and apply descriptive statistic measures on the column 'pulse' (analogue to pandas' describe() method):")

# Define function for calculation descriptive statistics.
def groupby_describe(df, groupby_col, stat_col):
    out = df.groupby(groupby_col).agg(
        F.mean(stat_col).alias("mean"),
        F.stddev(stat_col).alias("std"),
        F.min(stat_col).alias("min"),
        F.expr(f"percentile({stat_col}, array(0.25))")[0].alias("low_quart"),
        F.expr(f"percentile({stat_col}, array(0.5))")[0].alias("median"),
        F.expr(f"percentile({stat_col}, array(0.75))")[0].alias("up_quart"),
        F.max(stat_col).alias("max"),
    )
    return out

# Apply function to df Dataframe
start_1 = time.time()
df_stats = groupby_describe(df, ['ts_number', 'category'], 'pulse')
end_1 = time.time()
# Show Dataframe output
df_stats.show()

print(f'Elapsed time (minutes) for calculating statistic measures: {(end_1-start_1)/60}')
print(f'Dataframe consists of {df_stats.count()} rows.')
print("")

## Encoding the target variable 'category'

print('Encoding "category" column and store as Target:')

start_2 = time.time()
catEncoder = StringIndexer(inputCol='category', outputCol='Target').fit(df_stats)
df_stats = catEncoder.transform(df_stats)
end_2 = time.time()

# Show Dataframe
df_stats.show()

print(f'Elapsed time (minutes) for encoding target variable: {(end_2-start_2)/60}')
print("")

## Transform features to a vector
print("Transform features to vector and store as 'features':")
required_features = ['mean', 'std', 'min', 'low_quart', 'median', 'up_quart', 'max', 'Target']

start_3 = time.time()
vec_assembler = VectorAssembler(inputCols=required_features, outputCol='features')
df_stats_vec = vec_assembler.transform(df_stats)
end_3 = time.time()

# Show Dataframe
df_stats_vec.show()
print(f'Elapsed time (minutes) for transforming features to vector: {(end_3-start_3)/60}')
print("")

## Split data set into training (70%) and test data set (30%)
print("Split Training and Test:")
start_4 = time.time()
train_df, test_df = df_stats_vec.randomSplit([0.7, 0.3], seed=12345)
end_4 = time.time()

print(f'Elapsed time (minutes) for splitting data into training and test set: {(end_4-start_4)/60}')
print(f"Number of train dataset: {train_df.count()}")
print(f"Number of test  dataset: {test_df.count()}")
print("")

## Apply Logistic Regression as Classification Model

print('Apply Logistic Regression model based on training data set and predict category on test data set:')

# Train and fit model
start_5 = time.time()
lr = LogisticRegression(featuresCol='features', labelCol='Target')
lr_model = lr.fit(train_df)
end_5 = time.time()
# Provide prediction based on  trained model.
start_6 = time.time()
y_pred = lr_model.transform(test_df)
end_6 = time.time()

# Show prediction vs. true values on test data set.
df_target_vs_prediction = y_pred.select('Target', 'prediction')
df_target_vs_prediction.show()

print(f'Elapsed time (minutes) for training logistic regression model: {(end_5-start_5)/60}')
print(f'Elapsed time (minutes) for predicting values on test data set: {(end_6-start_6)/60}')
print("")


# Model Evaluation
print("Model evaluation measures:")
start_7 = time.time()
multi_evaluator_acc = MulticlassClassificationEvaluator(labelCol='Target', metricName='accuracy')
print(f'Prediction Accuracy: {multi_evaluator_acc.evaluate(y_pred)}')
multi_evaluator_prec = MulticlassClassificationEvaluator(labelCol='Target', metricName='weightedPrecision')
print(f'Prediction Precision: {multi_evaluator_prec.evaluate(y_pred)}')
multi_evaluator_rec = MulticlassClassificationEvaluator(labelCol='Target', metricName='weightedRecall')
print(f'Prediction Recall: {multi_evaluator_rec.evaluate(y_pred)}')
multi_evaluator_f1 = MulticlassClassificationEvaluator(labelCol='Target', metricName='f1')
print(f'Prediction F1-Score: {multi_evaluator_f1.evaluate(y_pred)}')
end_7 = time.time()

print(f'Elapsed time (minutes) for calculating evaluation measures: {(end_7-start_7)/60}')
print("")


end_all = time.time()
print(f'Elapsed time (minutes) for whole process: {(end_all-start_all)/60}')