import boto3
import json
from datetime import datetime
from kafka import KafkaConsumer


s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9002",
    aws_access_key_id="admin",
    aws_secret_access_key="password123"
)


bucket_name = "bronze-transactions"



try:
    s3.head_bucket(Bucket=bucket_name)
    print(f"Bucket {bucket_name} already exists.")
except:
    s3.create_bucket(Bucket=bucket_name)
    print(f"Created bucket {bucket_name}.")



consumer = KafkaConsumer(
    "stock-quotes",
    bootstrap_servers=["localhost:29092"],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="bronze-consumer1",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)


print("Consumer streaming and saving to MinIO...")



for message in consumer:
    record = message.value
    symbol = record.get("symbol", "unknown")
    print(symbol)
    ts = record.get("fetched_at", datetime.now())
    key = f"{symbol}/{ts}.json"

    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=json.dumps(record),
        ContentType="application/json"
    )
    print(f"Saved record for {symbol} = s3://{bucket_name}/{key}")