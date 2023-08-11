from fastapi import FastAPI, HTTPException, Query
import psycopg2
from datetime import datetime
import urllib.parse
import requests
from bs4 import BeautifulSoup
import os

app = FastAPI()

# Database connection parameters
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# Password to authenticate deletion
delete_password = os.getenv("DELETE_PASSWORD")


def delete_submission_from_database(url):
    try:
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password,
        )

        cursor = connection.cursor()

        delete_query = "DELETE FROM submissions WHERE url = %s"
        cursor.execute(delete_query, (url,))

        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Submission deleted successfully"}

    except Exception as e:
        return {"message": f"Error: {e}"}

def delete_submission_from_database(url):
    try:
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password,
        )

        cursor = connection.cursor()

        delete_query = "DELETE FROM submissions WHERE url = %s"
        cursor.execute(delete_query, (url,))

        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Submission deleted successfully"}

    except Exception as e:
        return {"message": f"Error: {e}"}

def get_jams_from_database():
    try:
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password,
        )

        cursor = connection.cursor()

        select_query = "SELECT jam, title, url, timeCreated FROM submissions"
        cursor.execute(select_query)
        jams = cursor.fetchall()

        cursor.close()
        connection.close()

        jam_list = []
        for jam in jams:
            jam_obj = {
                "jam": jam[0],
                "title": jam[1],
                "url": jam[2],
                "timeCreated": jam[3]
            }
            jam_list.append(jam_obj)

        return jam_list

    except Exception as e:
        return {"message": f"Error: {e}"}


def get_title_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else None
        return title
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def save_submission_to_database(jam_slug, title, url):
    try:
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password,
        )

        cursor = connection.cursor()

        insert_query = """
        INSERT INTO submissions (jam, title, url, timeCreated) 
        VALUES (%s, %s, %s, %s)
        """
        current_time = datetime.now()
        cursor.execute(insert_query, (jam_slug, title, url, current_time))

        connection.commit()
        cursor.close()
        connection.close()

        return {"message": "Submission saved successfully"}

    except Exception as e:
        return {"message": f"Error: {e}"}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/submitJam/{jam_slug}/{finishedURL:path}")
async def submit_jams(jam_slug: str, finishedURL: str):
    try:
        decoded_url = urllib.parse.unquote(finishedURL)
        title = get_title_from_url(decoded_url)

        if title:
            save_submission_to_database(jam_slug, title, decoded_url)
            return {"message": "Submission successful"}
        else:
            return {"message": "Title not found."}

    except Exception as e:
        return {"message": f"Error: {e}"}

@app.get("/getJams")
async def get_jams():
    jams = get_jams_from_database()
    return jams

@app.delete("/deleteSubmission")
async def delete_submission(url: str, password: str = Query(...)):
    if password != delete_password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    result = delete_submission_from_database(url)
    return result
