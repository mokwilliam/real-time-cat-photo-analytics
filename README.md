# Real-time Cat Photo Analytics
This small project focuses on the use of Apache Airflow and Kafka.

Help from https://airflow.apache.org/ and https://kafka.apache.org/.

## Overview
This project involves building a real-time data pipeline that simulates events for cat photos, including views and likes. I'll use the website [CatAPI](https://thecatapi.com/) (for more details, go check the [docs](https://developers.thecatapi.com/)) to fetch cat images at regular intervals, simulate user interactions, and stream the data using Apache Kafka. The data will be stored in a simple JSON file.

## Steps followed

### 0. Installation & Setup
For Apache Airflow:
```bash
pip install apache-airflow

# Modify the AIRFLOW_HOME in the project directory
export AIRFLOW_HOME=$(pwd)/airflow

# Initialize the Airflow database at $AIRFLOW_HOME
airflow db init

# If it's the first time, we must set an user
airflow users create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin

# Start the Airflow web server and scheduler (in two terminals)
airflow webserver -p 8080
airflow scheduler
```

For Apache Kafka (https://kafka.apache.org/downloads):
```bash
# Setup in our PATH (e.g. in the .bashrc)
# For instance
export KAFKA_HOME=$(pwd)/apache_kafka
export PATH=$KAFKA_HOME/bin:$PATH
```

### 1. Modify the config file for the Apache Airflow webserver
When the initialization of the Airflow database done, we can access to the config file. Inside we can check the default configuration.

Changes made:
```python
load_examples = False
default_timezone = Europe/Paris
expose_config = True
dags_are_paused_at_creation = False
```

### 1bis. Start the Kafka environment
```bash
# Start ZooKeeper
apache_kafka/bin/zookeeper-server-start.sh apache_kafka/config/zookeeper.properties

# Start Kafka
apache_kafka/bin/kafka-server-start.sh apache_kafka/config/server.properties
```

### 2. Create DAG (Directed Acyclic Graph)
I retrieved data from the following website https://thecatapi.com/.

```python
# Default arguments for the DAG
# ...

# Create a DAG instance
# ...
```

### 3. Create a Kafka topic to store events
```bash
apache_kafka/bin/kafka-topics.sh --create --topic cat_photo_events --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 4. Implement the Kafka Producer and Consumer
- **Producer**: those client applications that publish (write) events to Kafka.
- **Consumer**: those that subscribe to (read and process) these events.

Python library `confluent-kafka` is used to create basic clients.
For more details, go check the [docs](https://docs.confluent.io/kafka-clients/python/current/overview.html) or [GitHub](https://github.com/confluentinc/confluent-kafka-python).

Check the content of `kafka_producer.py` and `kafka_consumer.py`.

### 5. Move the DAG Python file into the right folder
Basically, by default, DAGs are located in `$AIRFLOW_HOME/dags` directory. So the `cat_photo_dag.py` must be inside this folder.

```bash
mkdir -p $AIRFLOW_HOME/dags
cp cat_photo_dag.py kafka_producer.py $AIRFLOW_HOME/dags
```

### 6. Run Python files
```bash
# Launch Kafka Producer thanks to Airflow (with two CLI)
airflow webserver -p 8080
airflow scheduler

# Launch Kafka Consumer manually
python kafka_consumer.py
```

### Where I got a bit stuck / Interesting points
- To check the list of DAGs, we can run `airflow dags list`.
- If there's a problem with DAGs, the command `airflow dags list-import-errors` provides the errors encountered.
- The timezone must be checked carefully. It may causes some problems, especially for the run of DAGs, it won't run automatically for instance.
- **TO CLARIFY** - I didn't find any solution concerning the DAG import error. Indeed, I've put the Kafka Producer file in the DAGs folder in order to make the DAG works. Maybe should I merge both file `cat_photo_dag.py` and `kafka_producer.py` ?

### Extra: Setup of pre-commit
```bash
pip install pre-commit
```

Once the `.pre-commit-config.yaml` completed, we need to set up the git hooks scripts.

```bash
pre-commit install
```