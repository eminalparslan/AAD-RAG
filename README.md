# AAD (American Academy of Dermatology) RAG

RAG system for documents from the AAD based on [llamaindex](https://github.com/run-llama/llama_index) and [streamlit](https://github.com/streamlit/streamlit).

## How to run/deploy

Install python dependencies:

`pip install -r requirements.txt`

Verify documents are in `./data/` directory.

Push to GitHub repo.

Navigate to [Streamlit Community Cloud](https://share.streamlit.io/), sign in, and create a new app from the GitHub repo.

During app creation, under advanced options, provide an OpenAI API key as a secret:

`openai_key = "<your OpenAI API key here>"`

Deploy!

## References

- https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/
