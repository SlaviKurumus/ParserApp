import os

import psycopg2
from dotenv import load_dotenv

from models import CREATE_TABLE_SQL


load_dotenv()


def get_connection():
    return psycopg2.connect(
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT"),
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(CREATE_TABLE_SQL)
    conn.commit()
    cur.close()
    conn.close()


def save_volunteer(data: dict):
    conn = get_connection()
    cur = conn.cursor()
    insert_query = """
        INSERT INTO volunteers (
            full_name, birth_date, profile_url, 
            volunteer_id,city, organization,
            social_links
        )
        VALUES (
            %(full_name)s, %(birth_date)s, %(profile_url)s,
            %(volunteer_id)s, %(city)s, %(organization)s,
            %(social_links)s
        )
        ON CONFLICT (profile_url) DO NOTHING;
    """
    cur.execute(insert_query, data)
    conn.commit()
    cur.close()
    conn.close()