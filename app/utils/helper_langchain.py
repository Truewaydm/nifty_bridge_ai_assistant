import os
from typing import Annotated

from fastapi import HTTPException, Header
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from app.utils.constants import API_KEY, INVALID_API_KEY, IS_VALID_TOKEN

if os.environ.get("DOCKER_ENV"):
    # Running in Docker container
    file_pdf = "/code/app/templates/Untitled5.pdf"
else:
    # Running locally
    file_pdf = "templates/Untitled5.pdf"


# Load the PDF document
def load_pdf_file():
    file_path = os.path.abspath(file_pdf)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    pdf_loader = UnstructuredPDFLoader(file_path=file_path)
    documents = pdf_loader.load()
    return documents


# Split the document into chunks for processing
def split_document(documents):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    chunks = text_splitter.split_documents(documents)
    return chunks


# Initialize the OpenAI embeddings and vectorstore
def initialize_embeddings_and_vectorstore(chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)
    return vectorstore


# Check API token
def validate_token(x_api_key_token: Annotated[str, Header()]):
    if x_api_key_token != API_KEY:
        raise HTTPException(status_code=401, detail=INVALID_API_KEY)
    else:
        return {"detail": IS_VALID_TOKEN}
