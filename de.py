import requests
import json
import psycopg2
from datetime import datetime, timedelta

conn = psycopg2.connect(
    host="localhost",
    database="stack_overflow",
    user="postgres",
    password="password"
)
cur = conn.cursor()

base_url = "https://api.stackexchange.com/2.3"
site = "stackoverflow"
key = "YOUR_API_KEY"

today = datetime.utcnow().date()
last_month = today - timedelta(days=30)

def get_tag_data(tag):
    url = f"{base_url}/questions?fromdate={int(last_month.timestamp())}&order=desc&sort=votes&tagged={tag}&site={site}&key={key}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data["items"]

def store_data(tag, data):
    for item in data:
        cur.execute("INSERT INTO stack_overflow_questions (tag, question_id, title, creation_date, score) VALUES (%s, %s, %s, %s, %s)",
                    (tag, item["question_id"], item["title"], datetime.fromtimestamp(item["creation_date"]), item["score"]))
    conn.commit()

tags = ["python", "java", "javascript", "php", "c++"]

for tag in tags:
    data = get_tag_data(tag)
    store_data(tag, data)
