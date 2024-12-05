from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI
import openai
import streamlit as st

st.set_page_config(page_title="Learn more about your diagnosis and treatment", layout="centered", initial_sidebar_state="auto", menu_items=None)
openai.api_key = st.secrets.openai_key
st.title("Learn more about your diagnosis and treatment")
st.info("Chat with documents from the American Academy of Dermatology (AAD) to learn more about your diagnosis and treatment.")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me about your diagnosis and treatment.",
        }
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    documents = SimpleDirectoryReader(input_dir="./data", recursive=True).load_data()
    Settings.llm = OpenAI(
        model="gpt-3.5-turbo",
        temperature=0.2,
        system_prompt="""You are an expert on dermatological conditions and treatments. You are helpful and honest. You answer questions based on the information provided in the documents. If you don't know the answer, you say "I don't know" and don't try to make up an answer. If you don't know the answer, don't try to make up an answer."""
    )
    index = VectorStoreIndex.from_documents(documents)
    return index

index = load_data()

if "chat_engine" not in st.session_state.keys():
    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode="condense_question", verbose=True, streaming=True
    )

if prompt := st.chat_input(
    "Ask a question about your diagnosis and treatment",
):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        response_stream = st.session_state.chat_engine.stream_chat(prompt)
        st.write_stream(response_stream.response_gen)
        message = {"role": "assistant", "content": response_stream.response}
        st.session_state.messages.append(message)

        if hasattr(response_stream, "source_nodes") and response_stream.source_nodes:
            st.write("Sources:")
            sources = set()
            for source_node in response_stream.source_nodes:
                sources.add(source_node.node.metadata["file_name"])
            for source in sources:
                source = source.replace("_", " ")
                st.caption(f"- {source}")

# query_engine = index.as_query_engine(
#     response_mode="tree_summarize",  # or "compact" or "refine"
#     include_source_nodes=True
#     # streaming=True,
#     # verbose=True
# )

# while True:
#     response = query_engine.query(input("> "))
#     print(f"Response: {response.response}\n")
#     print("Sources:")
#     for source_node in response.source_nodes:
#         print(f"File: {source_node.node.metadata['file_name']}")
#         # print(f"Content: {source_node.node.text[:200]}...\n")
