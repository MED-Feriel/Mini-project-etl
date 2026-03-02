import os
import logging
import requests
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def extract():
    url = "https://jsonplaceholder.typicode.com/posts"
    logging.info("Extracting data...")
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def transform(data):
    logging.info("Transforming data...")
    df = pd.DataFrame(data)
    df = df[['userId', 'id', 'title']]
    return df

def load(df):
    logging.info("Loading into PostgreSQL...")
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            user_id INT,
            post_id INT PRIMARY KEY,
            title TEXT
        );
    """)

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO posts (user_id, post_id, title)
            VALUES (%s, %s, %s)
            ON CONFLICT (post_id) DO NOTHING;
        """, (row['userId'], row['id'], row['title']))

    conn.commit()
    conn.close()

def export_csv(df):
    logging.info("Exporting CSV...")
    df.to_csv("posts.csv", index=False)

if __name__ == "__main__":
    data = extract()
    df = transform(data)
    load(df)
    export_csv(df)
    logging.info("Pipeline completed successfully.")
