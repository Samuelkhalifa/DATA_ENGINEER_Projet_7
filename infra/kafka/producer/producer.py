import os
import json
import requests
import time
from dotenv import load_dotenv
from datetime import datetime
from kafka import KafkaProducer



load_dotenv()



API_KEY = os.getenv("API_KEY") 
BASE_URL = "https://finnhub.io/api/v1"
SYMBOLS = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]



producer = KafkaProducer(
    bootstrap_servers=["localhost:29092"], 
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)



def fetch_quote(symbol):
    url = f"{BASE_URL}/quote?symbol={symbol}&token={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        data["symbol"] = symbol
        data["fetched_at"] = datetime.now().isoformat()
        return data
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None




while True:
    for symbol in SYMBOLS:
        quote = fetch_quote(symbol)
        if quote:
            print(f"Producing: {quote}")
            producer.send("stock-quotes", value=quote)
    time.sleep(120)