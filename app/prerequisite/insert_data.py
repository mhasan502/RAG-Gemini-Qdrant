import logging
import unicodedata
import qdrant_client
from langchain_community.document_transformers.beautiful_soup_transformer import BeautifulSoupTransformer
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader


async def retrive_cleaned_docs() -> list:
    """
    Collects data from URL and clean it.

    :return: Cleaned pages content
    """
    try:
        loader = RecursiveUrlLoader(
            url="https://gigalogy.com/",
            use_async=False,
            max_depth=3,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": "Chrome/123.0.0.0",
            },
            extractor=lambda x: unicodedata.normalize("NFKC", x),
        )

        docs = loader.load()

        transformed_docs = BeautifulSoupTransformer().transform_documents(
            docs,
            unwanted_tags=["script", "style", "a", "footer", "header", "link"],
            tags_to_extract=["p", "h1", "h2", "h3", "h4", "h5", "h6", "span", "div", "section"]
        )

        filtered_docs = [
            (
                f"It is about Gigalogy and it says about it that {doc.metadata['title']}."
                f" In Gigalogy, {doc.metadata['description'] if 'description' in doc.metadata else ''}. "
                f"{doc.page_content[:-63]}"
            ) for doc in transformed_docs if len(doc.page_content) > 10
        ]

        return filtered_docs

    except Exception as e:
        logging.error(e)
        raise e


async def collect_data(client: qdrant_client.QdrantClient) -> None:
    """
    Collects data from Gigalogy website and enters it into the database.

    :return:
    """

    client.add(
        collection_name="gigalogy",
        documents=await retrive_cleaned_docs()
    )

    logging.info("Data has been entered to Database successfully")
