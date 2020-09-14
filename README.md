# Twitter-Bots-Identification
Classification of bots and legitimate users on Twitter using Kafka, MongoDB and Spark.

Run this before testing.

Terminal Window 1:
$ zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties

Terminal Window 2:
$ kafka-server-start /usr/local/etc/kafka/server.properties

Terminal Window 3:
$ kafka-topics --zookeeper localhost:2181 --list 
$ kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic bots

To delete the topic:
// run the command below at the end of testing
$ kafka-topics --delete --zookeeper localhost:2181 --topic bots

Code Description:

Kafka Producer:
	1. producer_stream.ipynb (Use direct twitter real time stream)
	2. producer_csv.ipynb  (Takes data from a CSV file)
	##	Run producer_stream.ipynb for real time streaming of data into Kafka

Kafka Consumer:	
	consumer.ipynb

Model Training and Bot prediction:
	project.ipynb	
