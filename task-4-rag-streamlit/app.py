import streamlit as st

from langchain_community.document_loaders import PDFPlumberLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""

save_directory = './documents/'

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = InMemoryVectorStore(embeddings)

model = OllamaLLM(model="llama3.2:1b")


def upload_file(file):
    with open(save_directory + file.name, "wb") as f:
        f.write(file.getbuffer())


def load_file(file_path: str):
    if file_path.endswith(".pdf"):
        loader = PDFPlumberLoader(file_path)
    elif file_path.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    else:
        loader = TextLoader(file_path, autodetect_encoding=True)
    documents = loader.load()

    return documents


def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )

    return text_splitter.split_documents(documents)


def index_docs(documents):
    vector_store.add_documents(documents)


def retrieve_docs(query):
    return vector_store.similarity_search(query)


def answer_question(question, documents, history):
    context = "\n\n".join([doc.page_content for doc in documents])
    context += "\n\n".join([
        f"{message["role"]}:{message["content"]}"
        for message in history
    ])
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    return chain.invoke({"question": question, "context": context})


uploaded_file = st.file_uploader(
    "Upload file",
    type=["pdf", "txt", "docx"],
    accept_multiple_files=False
)

if uploaded_file:
    upload_file(uploaded_file)
    documents = load_file(save_directory + uploaded_file.name)
    chunked_documents = split_text(documents)
    index_docs(chunked_documents)

    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        st.chat_message(message["role"]).write(message["content"])

    question = st.chat_input()

    if question:
        st.chat_message("user").write(question)
        st.session_state.messages.append(
            {"role": "user", "content": question})
        related_documents = retrieve_docs(question)
        answer = answer_question(
            question, related_documents, st.session_state.messages)
        st.chat_message("assistant").write(answer)
        st.session_state.messages.append(
            {"role": "assistant", "content": answer})
