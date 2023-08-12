from fastapi import FastAPI, Response, status
import jamsapi.router.openai as openai_requests

app = FastAPI(
    title="JAMS API",
    description="An API for Jams services and an API gateway for other needed services.",
    version="0.0.1",
    contact={
        "name": "Arpan Pandey",
        "email": "arpan@hackclub.com"
    }

)

@app.get("/")
def root():
    return {"message": "Hello World, from JAMS API! Head over to /docs or /redoc to see the API documentation."}


@app.get("/openai/models")
def models(response: Response):
    """
        Get the list of models available on OpenAI API
    """
    response.status_code = openai_requests.models()[1]
    return openai_requests.models()[0]

@app.get("/openai/models/{model_name}")
def model(model_name: str, response: Response):
    """
        Get the details of a model available on OpenAI API
    """
    response.status_code = openai_requests.model(model_name)[1]
    return openai_requests.model(model_name)[0]

@app.post("/openai/chat/completions")
def post_chat_completions(data: dict, response: Response):
    """
        Post a chat to OpenAI API
    """
    response.status_code = openai_requests.post_chat_completions(data)[1]
    return openai_requests.post_chat_completions(data)[0]

@app.post("/openai/images/generations")
def create_image(data: dict, response: Response):
    """
        Create an image on OpenAI API
    """
    response.status_code = openai_requests.create_image(data)[1]
    return openai_requests.create_image(data)[0]


@app.post("/openai/embeddings")
def embeddings(data: dict, response: Response):
    """
        Get the embeddings of a text on OpenAI API
    """
    response.status_code = openai_requests.embeddings(data)[1]
    return openai_requests.embeddings(data)[0]