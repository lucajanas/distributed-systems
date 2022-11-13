Requirements:
- docker: https://docs.docker.com/desktop/install/windows-install/
- docker-compose: https://docs.docker.com/compose/install/


Steps:

If you want to download the already built image:  

      docker pull lucajanas/spark

If you want to build the image yourself (which may take a while)

      cd distributed-systems/build
      docker build . -t lucajanas/spark

To run the containers:

      cd distributed-systems
      docker-compose up -d --scale spark-worker=<number-of-workers>, e. g. 
      
      docker-compose up -d --scale spark-worker=2

Go to localhost:8888 in your browser to access JupyterLab and work with pyspark. 

Before you start, please download the six files from GoogleDrive link https://drive.google.com/drive/folders/1yvU4RxPRLoy-KmEMYfy-Ibn0SjIPHD5_?usp=share_link
and upload them to the JupyterLab environment.

Run the notebook 

    load_simulation_data/Cross-sectional time series classification.ipynb 

to start the analysis process.



To stop the containers, run

    docker-compose down

# Guiding questions

1. What are the central components in your system? Describe the architecture of the constructed information system, name the central software components in your solution, and describe their purpose.

Our system consists of one containerized spark master and two containerized spark workers, controlled by docker-compose running on a single machine. You can submit spark applications to this cluster / the spark master by creating a SparkContext using pyspark from your local machine. The spark master distributes the requests to a worker with enough available resources to handle the request from the client (your local machine). The tasks assigned to a spark worker are then handled / processed by an executor within the spark worker.

![image](https://user-images.githubusercontent.com/58073358/197608242-660a6ee2-cc12-442d-b6d3-68aa0a5e4964.png)

Source: https://spark.apache.org/docs/latest/cluster-overview.html

2. What is the analytical problem that you want to solve? Present an adequate formal definition of your problem and describe the process how you solve it using the prototypical implementation in your data pipeline.

We want to apply a classification problem to several labeled time series and make predictions based on them. For this purpose, we have generated a number of time series datasets. We have simulated the daily resting heart rate measurements, respectively the resting pulse, in beats per minute (bpm) of fictitious subjects from January 2021 to March 2021. To ensure that these values are comparable throughout the day, we emphasize that pulse measurements are always taken at the time after waking up from sleep overnight. For each subject, these are 90 observations with equidistant intervals with no missing values. In particular, we distinguish subjects with different fitness levels. Studies have shown that significantly lower resting pulses are measured in athletes and for example people who do endurance training or yoga (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6306777/).
Therefore, for the label of the time series, we consider the three categories of subjects: 
- 'pro_athletes' as professional athletes
- 'athletes' as regular hobby athletes
- 'non_athletes' as non-athletes who do little to no exercise. 

The observations are simulated by normally distributed random draws. Here, the means and standard deviations also depend on a normally distributed random draw.
On average, it is simulated that the group of 'pro_athletes' has a resting pulse of 50, the group of 'athletes' has one of 65 and the 'non_athletes' has one of 80. The exact data simulation is implemented in the python file 'load_simulation_data.py'.

For our big data use case, we have a total of 13,500,000 records consisting of 150,000 labeled subjects (divided into 6 csv files). Each file reaches a file size of 735 MB to 761 MB.
You can download them here (https://drive.google.com/drive/folders/1yvU4RxPRLoy-KmEMYfy-Ibn0SjIPHD5_?usp=share_link).

The formal definition of our problem is how can we build an accurate classifier based on derived features from the time series to predict the categories of different fitness levels.

To solve this problem, we first need to preprocess the data appropriately for our classification problem and do feature engineering.
Thus, we need to define aggregate measures for each of the time series which we can use as independent variables for fitting the model to estimate the target variable as well as possible.
To do this, we aggregate all the resting pulse observations for each subject, so that we use
- the arithmetic mean 'mean'
- the standard deviation 'std'
- the minimum 'min'
- the lower quartile (25% quantile) 'low_quart'
- the median 'median'
- the upper quartile (75% quantile) 'up_quart'
- the maximum 'max'

as features in our model.

For the use of logistic regression the expressions of the target variable must be encoded to 0, 1 and 2 since we have multinomial output.
Analogue to a binary logistic regression where we must encode the variable to 0 and 1. The use of multinomial logistic regression is explained in more detail in question 3.
As the next step, we need to vectorize the feature columns and store them into a column, which we call 'features' using the VectorAssembler function to transform them.

For training our model and evaluating the model goodness on the test data, it is necessary to randomly divide our dataset into training and test data. In this case, we use 70% of the data for training our model and the remaining 30% we use for our test validation. For a reproducible result, we have fixed a seed value.

We can now use the pyspark.ml.classification module to apply multinomial logistic regression on our training dataset. 
On this trained model we can apply our test data set and compare the predicted values with the true output values from the test data.
Since we have systematically simulated our data, it is not surprising that we have produced a model with a very good predictive power. 
This result is reflected in the evaluation measures explained in question 4. 

3. How does your analytical approach work and what changed compared to a non distributed version of the algorithm? Describe the algorithm that you chose to derive a solution with a focus on the tradeoffs that have been made in the distributed environment.

The algorithm we chose to derive a solution is multinomial logistic regression. 
Typically, logistic regression is used for binary outcome prediction. 
In our case, we have three categorical outcomes, so that's why we resort to multinomial logistic regression. 
For simplicity, we will use binary logistic regression first for the explanation, since the multinomial version is based on it. 
Logistic regression is a parametric classification model from supervised learning. 
It is derived from the idea of linear regression. 
Since we do not want to predict an interval scaled target variable as in linear regression, we transform the function in such a way that we congest it into a sigmoid function to obtain probabilities for the occurrence of an outcome 0 or 1. 
For a threshold, we usually consider the cutoff at 0.5 for the classification decisions for 0 or 1. 
What this fit should look like depends on the independent variables, the features. 
The parameters are calculated depending on the available training data. 
The fitted model can be used to read in new input data and estimate the outcome of the target variable. 
For the application of multinominal logistic regression, a separate binary regression is calculated in the background for each outcome category, where the selected outcome is assigned as 1 and all others as 0. 
For the prediction of the outcome, the outcome with the highest probability is selected for each calculated binary logistic regression.

In a non distributed version this analytical approach would run slower. Due to its distributed architecture in a cluster using Spark, we can process extremely large amounts of data in a performant manner and thus execute jobs in parallel.
It is easily scalable and works in memory. However, if you are processing small amounts of data, the computation may be slower because the loading of data is done by multiple tasks, where each task is loaded into multiple partitions.
The distributed system has the advantage that the data is replicated on several machines and thus protected against data loss in the event of a machine failure.

There are also a fewer tradeoffs in using the distributed environment using spark.
In the non-distributed environment the pandas library is one of the most used and most powerful data analysis and data manipulation tool.
In the distributed environment using spark we must resort to using pyspark dataframes in python. 
Unfortunately, the pyspark dataframes has a limited support of pandas dataframe functions. 
For instance when calculating the statistics for each time series using column id 'ts_number', we could not just apply the implemented describe() function as it is possible in the pandas dataframe setting.
That is why we have defined a function groupby_describe() in our project for calculating the statistics using the module pyspark.sql.functions.
Another aspect in the application of spark is, that spark seems to be slow in a few situations, especially by counting the rows in a spark dataframe.
That's why in our notebook the counting calculations are commented out. If you are interested in the output, just comment them back in.

4. How can your solution be evaluated? Discuss how the quality of your analytical solution can be evaluated and present some evaluation statistics as results. The actual quality of your forecasts or classification is not of interest, but the process on how to derive evaluation statistics and how one would benchmark multiple models.

Since we have chosen a multinomial logistic regression model with nominally scaled outcome variables as our analytic approach, we can consider a confusion matrix to measure correctly classified and misclassified predictions. From this confusion matrix, we can apply various statistical measures to evaluate our model based on the training data on the test data.

- Accuracy: The accuracy measure is defined as the percentage of correctly classified data of all prediction outcomes in the test data.

But the accuracy measure is not a good measure for unbalanced classification. Therefore, it is often necessary to consider other metrics.

- Precision: Precision is a metric that shows how many of the positive predictions made are correct.

- Recall: Recall is a metric that shows how many of the positive cases the classifier has correctly predicted, over all the positive cases in the data.

- F1-Score: A good classifier is a good tradeoff of both precision and recall to be close to the value 1. Therefore, the F1-score metric is needed to combine both precision and recall.

5. What are the limitations of your solution? Kleppmann (2017) mentions reliability, scalability, and maintainability as key success factors for distributed data intensive systems. How are those goals achieved in your system? What are the most relevant topics (e.g. sections or subsections from Kleppmanns book) when scaling your prototypical system?

Our docker-compose setup is neither highly available nor scalable or very maintainable as it is intended more as a prototype / testing environment. The containers controlled by docker-compose still run on a single machine, which leads to complete unavailability of the service in case this single machine fails, e. g. due to hardware failure. We have redundant spark workers, so if one of these workers fails due to internal problems, there still should be a backup worker which the master can forward requests to. We do not have a redundant spark master. In case of failure of the spark master, the complete service is not available. In order to reduce the risk of human errors, spark offers clients in many different languages such as Python, Java, Spark and R which offer abstracted functions to submit spark applications.

The scalability of our system is limited by the resources available on the local machine which runs the containers. Nevertheless, more spark workers can be added to the system by adjusting the docker-compose.yml until the resources of the local machine are used up.

The disadvantages and weaknesses of our system in regards to reliability and scalability could be dealt with by running spark in a kubernetes cluster with multiple physical nodes / virtual machines in it. Hereby, there could be redundant master and worker nodes in kubernetes which can handle the workload even in case one or more machine fails. With multiple machines in the kubernetes cluster, the scalability of the system would not be limited to the resources of a single machine. In addition, more nodes can be added to the kubernetes cluster quite easily to increase the available resources in case the cluster resources are exhausted. This addition (and possibly removing) of nodes can even happen dynamically depending on the resource utilization of the cluster. Hereby, temporary load peaks could be handled.

Regarding maintailability, updating the spark version is fairly easy. You just have to update the version of the spark container in the docker-compose.yml. But changing something in this setup requires a restart and therefore a downtime of the application. Here, too, kubernetes could possibly help by introducing rolling updates of the service. With rolling updates, kubernetes pods with the new spark version could be rolled out while the pods with the old version keep serving clients until the new spark version takes over.

Nevertheless, using the containerized version of spark removes a part of the complexity even in our docker-compose setup as the container images bring everything spark needs and can be tested as a whole. To improve the maintainability of our system, monitoring - e. g. using prometheus and grafana - would be very helpful.
