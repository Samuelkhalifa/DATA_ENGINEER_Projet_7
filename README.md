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

<br>

## [Subject : Build a complete ETL-process and data pipeline by using kafka streaming, containerization with Docker and Airflow orchestration, to serve finnhub-API market quotes data]

<br>

## &#x1F4DD; Project graph

<br>

<p align="center";>
  <img width="1219" height="419" alt="Capture d’écran 2026-04-16 à 22 06 24" 
  src="https://github.com/user-attachments/assets/c3cb21e4-798e-42d7-82b3-79c3b9e2748c" />
</p>

<br>

## &#127919; Project steps

<br>

  * Retrieve data from finnhub-API.
  * Transform data with `Python`.
  * Set up docker with a docker-compose.yml file and configurate all necessary services (`Kafka`and `Zookeeper` for streaming, also a kafka UI `kafdrop`, `airflow` webserver and scheduler for orchestration.
  * Initialize dbt and writes SQL queries for bronze, silver, and gold transformation to get production-ready data.
  * Activate airflow dag to make data travel from API source to snowflake, and transform it with `dbt`.

<br>

## &#128640; Project setup and activation

<br>

`Git clone` the project and get inside, to project root.
  ```bash
  git clone <repository-url> market-quotes-data-pipeline
  cd market-quotes-data-pipeline
  ```
<br>

Create and virtual environment
  ```bash
  python -m venv .venv
  source .venv/bin/activate  # (Mac/Linux)
  venv\Scripts\activate      # (Windows)
  ```

<br>

Install necessay packages written in requirement file
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


Enable `docker` by running the `docker-compose` file, which will create all necessary services, volumes and networks.
  ```bash
  docker-compose up
  ```
<br>

Go to `localhost:8080` to trigger your `Airflow` dag and start orchestrationg ELT process.

Go to `localhost:8080` to trigger your `Airflow` dag and start orchestrationg ELT process.

Go to `localhost:8080` to trigger your `Airflow` dag and start orchestrationg ELT process.

Go to `localhost:8080` to trigger your `Airflow` dag and start orchestrationg ELT process.
