import os
import logging
import decouple
import qdrant_client.http.exceptions
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from .utils import retrive_result
from .db_config import client
from .prerequisite import collect_data


os.environ["GOOGLE_API_KEY"] = decouple.config("GOOGLE_API_KEY")
app = FastAPI()
llm: ChatGoogleGenerativeAI


@app.on_event("startup")
async def startup() -> None:
    """
    Start up event before running the app.

    Inserts 'Gigalogy' collection to database if not exist.

    :return:
    """
    global llm
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    try:
        client.get_collection("gigalogy")
        logging.info("Gigalogy collection already exist.")
    except qdrant_client.http.exceptions.UnexpectedResponse:
        await collect_data(client)
        logging.info("Collected and Saved Gigalogy data.")


@app.post("/ask")
async def ask_gemini(question: str) -> JSONResponse:
    """
    Ask a question to the model and get response from LLM.

    :param question:
    :return: JSONResponse of the questions from LLM.
    """

    try:
        response = llm.invoke([HumanMessage(content=retrive_result(question=question))]).content
    except Exception as e:
        logging.error(e)
        raise e

    json_compatible_item_data = jsonable_encoder({
        "response": " ".join(response.split())
    })
    return JSONResponse(json_compatible_item_data)
