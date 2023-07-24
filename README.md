# FastAPI App

Fast App using LangChain framework

This is a FastAPI app that interacts with the OpenAI API and performs similarity search on a vectorstore. It provides an endpoint for sending a message and receiving a response.

[LangChain docs](https://python.langchain.com/docs/get_started/introduction.html)

## Prerequisites

- Python 3.10
- OpenAI API key

## Usage

You can deploy the project via Docker.

[Docker website](https://www.docker.com/).

[install Docker Desktop](https://www.docker.com/products/docker-desktop/).

### Getting Started
Clone this repository:

```bash
git clone git@github.com:Truewaydm/nifty_bridge_ai_assistant.git
````

Install the dependencies:

```bash
pip install -r requirements.txt
 ````
#### Environment

`.env`

```
OPENAI_API_KEY={Add OpenAI API key}
MODEL_NAME=gpt-3.5-turbo
```

### Run
#### Using Docker

```bash
>> docker-compose up -d --build

...
...
...
src_api_1 ... done
```
#### Without Docker
```bash
uvicorn app.main:app --host 0.0.0.0 --port 3000 --reload
```

Open Swagger documentation - http://127.0.0.1:3000/docs

We use the chatGPT 3.5 API to communicate with a PDF file, 
we can request any information contained in this file.

For example:
```
Request:
curl --location 'http://localhost:3000/api/send' \
--header 'x-api-key-token: {Add OpenAI API key}' \
--header 'Content-Type: application/json' \
--data '{
  "message": "Hello"
}'
---------------------------------------------------
Response:
{
"message": "Hello I am NiftyBridge AI assistant. How could I help you?"
}
```