Requirements:
- docker: https://docs.docker.com/desktop/install/windows-install/


Steps:

If you want to download the already built image:  

      docker pull lucajanas/spark

If you want to build the image yourself (which may take a while)

      cd distributed-systems/build
      docker built . -t lucajanas/spark

To run the containers:

      cd distributed-systems
      docker-compose up -d --scale spark-worker=<number-of-workers>, e. g. 
      
      docker-compose up -d --scale spark-worker=2

Go to localhost:8888 in your browser to access JupyterLab and work with pyspark. See 

    load_simulation_data/load_example.ipynb 

for an example on how to connect to the spark instance.

To stop the containers, run

    docker-compose down

# Guiding questions

1. What are the central components in your system? Describe the architecture of the constructed information system, name the central software components in your solution, and describe their purpose.

Our system consists of one containerized spark master and two containerized spark workers, controlled by docker-compose running on a single machine. You can submit spark applications to this cluster / the spark master by creating a SparkContext using pyspark from your local machine. The spark master distributes the requests to a worker with enough available resources to handle the request from the client (your local machine). The tasks assigned to a spark worker are then handled / processed by an executor within the spark worker.

![image](https://user-images.githubusercontent.com/58073358/197608242-660a6ee2-cc12-442d-b6d3-68aa0a5e4964.png)

Source: https://spark.apache.org/docs/latest/cluster-overview.html

2. What is the analytical problem that you want to solve? Present an adequate formal definition of your problem and describe the process how you solve it using the prototypical implementation in your data pipeline.

We want to apply a classification problem to several labeled time series and make predictions based on them. For this purpose, we have generated a number of time series datasets. We have simulated the daily resting heart rate measurements, respectively the resting pulse, in beats per minute (bpm) of fictitious subjects from January 2021 to March 2021. To ensure that these values are comparable throughout the day, we emphasize that pulse measurements are always taken at the time after waking up from sleep overnight. For each subject, these are 90 observations with equidistant intervals with no missing values. In particular, we distinguish subjects with different fitness levels. Studies have shown that significantly lower resting pulses are measured in athletes and people who do endurance training or yoga, for example (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6306777/).
Therefore, for the label of the time series, we consider the three categories of subjects: 
- 'pro_athletes' as professional athletes
- 'athletes' as regular hobby athletes
- 'non_athletes' as non-athletes who do little to no exercise. 

The observations are simulated by normally distributed random draws. Here, the means and standard deviations also depend on a normally distributed random draw.
On average, it is simulated that the group of 'pro_athletes' has a resting pulse of 50, the group of 'athletes' has one of 65 and the 'non_athletes' has one of 80. The exact data simulation is implemented in the python file 'load_simulation_data.py'.

For our big data use case, we have a total of 13,500,000 records consisting of 150,000 labeled subjects (divided into 6 csv files).

The formal definition of our problem is how can we build an accurate classifier based on derived features from the time series to predict the categories of different fitness levels.

3. How does your analytical approach work and what changed compared to a non distributed version of the algorithm? Describe the algorithm that you chose to derive a solution with a focus on the tradeoffs that have been made in the distributed environment.

4. How can your solution be evaluated? Discuss how the quality of your analytical solution can be evaluated and present some evaluation statistics as results. The actual quality of your forecasts or classification is not of interest, but the process on how to derive evaluation statistics and how one would benchmark multiple models.

Since we have chosen a multinomial logistic regression model with nominally scaled outcome variables as our analytic approach, we can consider a confusion matrix to measure correctly classified and misclassified predictions. From this confusion matrix, we can apply various statistical measures to evaluate our model based on the training data on the test data.

- Accuracy: The accuracy measure is defined as the percentage of correctly classified data of all prediction outcomes in the test data.

But the accuracy measure is not a good measure for unbalanced classification. Therefore, it is often necessary to consider other metrics.

- Precision: Precision is a metric that shows how many of the positive predictions made are correct.

- Recall: Recall is a metric that shows how many of the positive cases the classifier has correctly predicted, over all the positive cases in the data.

- F1-Score: A good classifier is a good trade of of both precision and recall to be close to the value 1. Therefore, the F1-score metric is needed to combine both precision and recall.

5. What are the limitations of your solution? Kleppmann (2017) mentions reliability, scalability, and maintainability as key success factors for distributed data intensive systems. How are those goals achieved in your system? What are the most relevant topics (e.g. sections or subsections from Kleppmanns book) when scaling your prototypical system?

Our docker-compose setup is neither highly available nor scalable or very maintainable as it is intended more as a prototype / testing environment. The containers controlled by docker-compose still run on a single machine, which leads to complete unavailability of the service in case this single machine fails, e. g. due to hardware failure. We have redundant spark workers, so if one of these workers fails due to internal problems, there still should be a backup worker which the master can forward requests to. We do not have a redundant spark master. In case of failure of the spark master, the complete service is not available. In order to reduce the risk of human errors, spark offers clients in many different languages such as Python, Java, Spark and R which offer abstracted functions to submit spark applications.

The scalability of our system is limited by the resources available on the local machine which runs the containers. Nevertheless, more spark workers can be added to the system by adjusting the docker-compose.yml until the resources of the local machine are used up.

The disadvantages and weaknesses of our system in regards to reliability and scalability could be dealt with by running spark in a kubernetes cluster with multiple physical nodes / virtual machines in it. Hereby, there could be redundant master and worker nodes in kubernetes which can handle the workload even in case one or more machine fails. With multiple machines in the kubernetes cluster, the scalability of the system would not be limited to the resources of a single machine. In addition, more nodes can be added to the kubernetes cluster quite easily to increase the available resources in case the cluster resources are exhausted. This addition (and possibly removing) of nodes can even happen dynamically depending on the resource utilization of the cluster. Hereby, temporary load peaks could be handled.

Regarding maintailability, updating the spark version is fairly easy. You just have to update the version of the spark container in the docker-compose.yml. But changing something in this setup requires a restart and therefore a downtime of the application. Here, too, kubernetes could possibly help by introducing rolling updates of the service. With rolling updates, kubernetes pods with the new spark version could be rolled out while the pods with the old version keep serving clients until the new spark version takes over.

Nevertheless, using the containerized version of spark removes a part of the complexity even in our docker-compose setup as the container images bring everything spark needs and can be tested as a whole. To improve the maintainability of our system, monitoring - e. g. using prometheus and grafana - would be very helpful.
