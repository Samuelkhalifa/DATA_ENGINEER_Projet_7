Project in the context of Data Engineering self-learning and inspired by Jay61616 with : <br>
github repo : <br>
https://github.com/Jay61616/real-time-stocks-mds and <br>
YouTube video : <br>
https://www.youtube.com/watch?v=JCDrvXwh4BQ&t=9078s


<br>

## &#128295; Used tools
![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![API](https://img.shields.io/badge/API-5BC0EB?style=for-the-badge)
![SQL](https://img.shields.io/badge/SQL-336791?style=for-the-badge)
![Bash](https://img.shields.io/badge/Bash-000000?style=for-the-badge&logo=gnubash&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=for-the-badge&logo=snowflake&logoColor=white)
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![MinIO](https://img.shields.io/badge/MinIO-C72E49?style=for-the-badge&logo=minio&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

<br>

## [Subject : Build a complete ELT-process and data pipeline by using kafka streaming, containerization with Docker and Airflow orchestration, to serve finnhub-API market quotes data]

<br>

## &#x1F4DD; Project graph

<br>

<p align="center";>
  <img width="1036" height="471" alt="Capture d’écran 2026-04-17 à 11 39 54" 
  src="https://github.com/user-attachments/assets/1c16e3e6-2ccb-4d9e-83e8-913045a3e66b" />
</p>

<br>

## &#127919; Project steps

<br>

  * Retrieve data from finnhub-API, with `Python`, inside the kafka producer and configure kafka consumer.
  * Set up docker with a docker-compose.yml file and configurate all necessary services (`Kafka`and `Zookeeper` for streaming, also a kafka UI `kafdrop`, `minIO` for initial bucket storage, `airflow` webserver and scheduler for orchestration, linked with a `postresql` database.
  * Initialize dbt and writes SQL queries for bronze, silver, and gold transformation to get production-ready data.
  * Write airflow dag's tasks to orchestrate the ELT process.
  * Run docker-compose to start data collect and bucket storage.
  * Trigger airflow dag to make data travel from API source to snowflake, and transform it with `dbt`.

<br>

## &#128640; Project setup and activation

<br>

`Git clone` the project and get inside, to project root.
  ```bash
  git clone <repository-url> market-quotes-data-pipeline

  cd market-quotes-data-pipeline
  ```
<br>

Create a virtual environment
  ```bash
  python -m venv .venv

  source .venv/bin/activate  # (Mac/Linux)
  venv\Scripts\activate      # (Windows)
  ```

<br>

Install necessary packages written in requirements file
  ```bash
  pip install -r requirements.txt
  ```

<br>

Write into a `env.` file your personal API key and credentials.
  ```bash
  touch .env # (for Mac)
  ```
  ```dotenv
  API_KEY=""

  MINIO_ENDPOINT="http://minio:9000"
  MINIO_ACCESS_KEY=""
  MINIO_SECRET_KEY=""
  BUCKET=""
  
  SNOWFLAKE_USER=""
  SNOWFLAKE_PASSWORD=""
  SNOWFLAKE_ACCOUNT=""
  SNOWFLAKE_WAREHOUSE="" 
  SNOWFLAKE_DB=""
  SNOWFLAKE_SCHEMA=""
  
  AIRFLOW_USER=  # with no quotes
  AIRFLOW_PASSWORD=  # with no quotes
  ```

<br>


Enable `docker` by running `start.sh`. Then the `docker-compose` file will be activated and will create all necessary services, volumes and networks.
  ```bash
  chmod +x init start.sh

  ./start.sh
  ```

<br>

Activate the Kafka consumer file, which will listen for next-activated kafka producer file
```bash
python infra/kafka/consumer consumer.py
```

<br>

Activate now the Kafka producer file
```bash
python infra/kafka/producer producer.py
```

<br>

Go to `localhost:9001` to monitor your `minIO` bucket storage results from kafka streaming.

Go to `localhost:9000` to monitor your `kafdrop` topics and other kafka activities.

Go to `localhost:8080` to trigger your `Airflow` dag and start orchestration to get the minIO into snowflake and transform it by dbt.

<br>

Go to `snowflake` plateform to manage your results.

  ```SQL
  USE <DATABASE>; # enable the database using

  TRUNCATE <TABLE>; # delete table to start from zero (if you retry)

  LIST @%<TABLE>; # be sure the stage table is empty (if you retry)

  SELECT * FROM <TABLE>;
  SELECT * FROM <VIEW>;
  ```

<br>

Open the `dashboard/.pbix` file.

Connect `Power Bi` to your `snowflake` database to use the dashboard.
