import jamsapi.openai.openai as openai_requests

from fastapi import FastAPI, HTTPException, Query, Response, Depends
from fastapi.responses import StreamingResponse
import psycopg2
from datetime import datetime
import urllib.parse
import requests
from bs4 import BeautifulSoup
from typing import Generator
import os
from fastapi.middleware.cors import CORSMiddleware
import jamsapi.openai.auth as openai_auth
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated

security = HTTPBearer()

app = FastAPI(
    title="JAMS API",
    description="An API for Jams services and an API gateway for other needed services.",
    version="0.0.1",
    contact={"name": "Arpan Pandey", "email": "arpan@hackclub.com"},
)

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


def get_submissions_from_database():
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
                "timeCreated": jam[3],
            }
            jam_list.append(jam_obj)

        return jam_list

    except Exception as e:
        return {"message": f"Error: {e}"}


def get_title_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        soup = BeautifulSoup(response.text, "html.parser")
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
def root():
    return {
        "message": "Hello World, from JAMS API! Head over to /docs or /redoc to see the API documentation."
    }


def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Authenticate the user using the token
    """
    sec = credentials.credentials

    if not openai_auth.validate_token(sec):
        return False

    if not openai_auth.use_token(sec):
        return True

    return sec


@app.get("/openai/models")
def models(
    response: Response,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    """
    Get the list of models available on OpenAI API
    """
    sec = authenticate(credentials)

    if not sec:
        response.status_code = 401
        return {"message": "Invalid token"}

    response.status_code = openai_requests.models()[1]
    return openai_requests.models()[0]


@app.get("/openai/models/{model_name}")
def model(
    model_name: str,
    response: Response,
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    """
    Get the details of a model available on OpenAI API
    """
    sec = authenticate(credentials)

    if not sec:
        response.status_code = 401
        return {"message": "Invalid token"}

    response.status_code = openai_requests.model(model_name)[1]
    return openai_requests.model(model_name)[0]


@app.post("/openai/chat/completions")
def post_chat_completions(
    data: dict, response: Response, credentials=Depends(security)
):
    """
    Post a chat to OpenAI API
    """
    sec = authenticate(credentials)

    if not sec:
        response.status_code = 401
        return {"message": "Invalid token"}

    resp = openai_requests.post_chat_completions(data)

    if resp[1] != 200:
        response.status_code = resp[1]
        return resp[0]


    return StreamingResponse(resp, media_type="application/json")


@app.post("/openai/images/generations")
def create_image(data: dict, response: Response, credentials=Depends(security)):
    """
    Create an image on OpenAI API
    """
    sec = authenticate(credentials)

    if not sec:
        response.status_code = 401
        return {"message": "Invalid token"}

    resp = openai_requests.create_image(data)
    return StreamingResponse(resp, media_type="image/png")


@app.post("/openai/embeddings")
def embeddings(data: dict, response: Response, credentials=Depends(security)):
    """
    Get the embeddings of a text on OpenAI API
    """

    sec = authenticate(credentials)

    if not sec:
        response.status_code = 401
        return {"message": "Invalid token"}

    resp = openai_requests.embeddings(data)
    return StreamingResponse(resp, media_type="application/json")


@app.get("/submitJam/{jam_slug}/{finishedURL:path}/{title}")
async def submit_jams(jam_slug: str, finishedURL: str, title: str):
    try:
        decoded_url = urllib.parse.unquote(finishedURL)
        if title:
            save_submission_to_database(jam_slug, title, decoded_url)
            return {"message": "Submission successful"}
        else:
            return {"message": "Title not found."}

    except Exception as e:
        return {"message": f"Error: {e}"}


@app.get("/getSubmissions")
async def get_submissions():
    jams = get_submissions_from_database()
    return jams


@app.delete("/deleteSubmission")
async def delete_submission(url: str, password: str = Query(...)):
    if password != delete_password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    result = delete_submission_from_database(url)
    return result
