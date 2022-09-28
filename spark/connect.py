import pyspark

conf = pyspark.SparkConf().setAppName('MyApp').setMaster('spark://localhost:7077')
sc = pyspark.SparkContext(conf=conf)

print('Submitted application!')