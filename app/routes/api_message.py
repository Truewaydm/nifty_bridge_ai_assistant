from fastapi import APIRouter, HTTPException

from app.models.message import Message
from app.utils.constants import API_KEY, MAX_TOKENS, MODEL_NAME, MAX_TOKEN_LIMIT
from app.utils.helper_langchain import load_pdf_file, split_document, initialize_embeddings_and_vectorstore
from langchain import OpenAI, PromptTemplate

app_message = APIRouter()


@app_message.post("/send", tags=["Message"])
def send_message(message: Message):
    """
    Endpoint for sending a message and receiving a response.

    Parameters:
    - message: The message to be sent (input)
    - x_api_key_token: API key token provided in the request header

    Returns:
    - Response: The generated response message
    """
    documents = load_pdf_file()
    chunks = split_document(documents)
    vectorstore = initialize_embeddings_and_vectorstore(chunks)

    query_message = message.message

    # Perform similarity search in the vectorstore and generate the answer
    docs = vectorstore.similarity_search(query_message)
    vectorstore_content = docs[0].page_content

    # Define the prompt template for generating the response
    prompt_template = """Answer the question based on the {vectorstore}. If the
    question cannot be answered using the information provided answer
    with "I don't know. Please contact support by email support@nifty-bridge.com".

    Context: {vectorstore} Hello I am NiftyBridge AI assistant. How could I help you?

    Question: {query_message}

    Answer: """
    # Initialize the Prompt template and Add prompt formatting variables
    prompt = PromptTemplate(template=prompt_template, input_variables=["query_message", "vectorstore"])
    prompt_formatting = prompt.format(query_message=query_message, vectorstore=vectorstore_content)

    # Initialize the OpenAI model and api key
    openai = OpenAI(model_name=MODEL_NAME, openai_api_key=API_KEY)

    # Generate the answer using the updated prompt formatting
    answer = openai(prompt_formatting)

    if openai.get_num_tokens(answer) > MAX_TOKENS:
        raise HTTPException(status_code=429, detail=MAX_TOKEN_LIMIT)

    # Handle the message and generate the response
    response = {"message": answer}
    return response
