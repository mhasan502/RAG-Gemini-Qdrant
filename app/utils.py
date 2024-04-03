import time
import logging
from .db_config import client

def retrive_result(question: str, query_limit: int = 5, retry_counter: int = 3) -> str:
    """
    Retrieves the result from the database and provides context for LLM.

    :param question:
    :param query_limit:
    :param retry_counter:
    :return: Metadata for LLM
    """
    result = []

    for i in range(retry_counter):
        try:
            result = client.query(
                collection_name="gigalogy",
                query_text=question,
                limit=query_limit,
            )
            break
        except Exception as e:
            if i == retry_counter - 1:
                logging.error(e)
                raise e
            else:
                time.sleep(1)

    context = "\n".join(r.document for r in result)

    return f"""
    You are a member of an Organization called 'Gigalogy Limited'. 
    The context provides the information regarding Gigalogy. 
    Answer the following question using the provided context regarding the organization. 
    Answer should be moderate in length.

    Question: {question.strip()}
    Context: {context.strip()}

    Answer:
    """
