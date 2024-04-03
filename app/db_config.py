import time
import logging
import decouple
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import ResponseHandlingException


def get_database_connection(retry_counter: int = 3) -> QdrantClient:
    """
    Get the database connection.

    :param retry_counter:
    :return: Qdrant database client
    """
    try:
        _client = QdrantClient(
            host=decouple.config("QDRANT_HOST"),
            port=decouple.config("QDRANT_PORT")
        )
        _client.get_collections()
        return _client
    except ResponseHandlingException as e:
        if retry_counter > 3:
            logging.error(e)
            raise e
        else:
            logging.error(e)
            retry_counter -= 1
            time.sleep(1)
            return get_database_connection()


client = get_database_connection()
