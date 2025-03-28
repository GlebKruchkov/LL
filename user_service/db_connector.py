from dotenv import load_dotenv
import os
import psycopg2
def DBConnection():
    load_dotenv()
    DB_Name = os.getenv('DB_NAME')
    DB_User = os.getenv('DB_USER')
    DB_Pass= os.getenv('DB_PASSWORD')
    DB_Host = os.getenv('DB_HOST')
    DB_Port = os.getenv('DB_PORT')
    try:
        conn = psycopg2.connect(
            database=DB_Name,
            user=DB_User,
            password=DB_Pass,
            host=DB_Host,
            port=DB_Port
        )
        print("Connected to PostgreSQL")
        return conn
    except Exception as e:
        print("Unable to connect to PostgreSQL", e)
        return None
