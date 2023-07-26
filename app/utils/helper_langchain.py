import os
from fastapi import HTTPException, Header
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from app.utils.constants import API_KEY, INVALID_API_KEY, IS_VALID_TOKEN, get_file_path


def load_pdf_file():
    """
    Load the PDF document
    """
    file_path = os.path.abspath(get_file_path("templates", "Untitled5.pdf"))
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    pdf_loader = UnstructuredPDFLoader(file_path=file_path)
    documents = pdf_loader.load()
    return documents


def split_document(documents):
    """
    Split the document into chunks for processing
    :param documents:
    :return: chunks
    """
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    chunks = text_splitter.split_documents(documents)
    return chunks


def initialize_embeddings_and_vectorstore(chunks):
    """
    Initialize the OpenAI embeddings and vectorstore
    :param chunks:
    :return: vectorstore
    """
    embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)
    return vectorstore


def validate_token(x_api_key_token: str = Header(...)):
    """
    Check API token
    :param x_api_key_token:
    :return: IS_VALID_TOKEN
    """
    if x_api_key_token != API_KEY:
        raise HTTPException(status_code=401, detail=INVALID_API_KEY)
    else:
        return {"detail": IS_VALID_TOKEN}
