from typing import Tuple
import ollama
from langchain_text_splitters import SentenceTransformersTokenTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from constants import (
    details
)


class ChatBot(object):
    def __init__(
        self,
        embed_model_name: str = "nomic-embed-text",
        chunk_overlap: int = 50,
        tokens_per_chunk: int = 200,
        model_name: str = "llama3.2:1b",
        context_details = str,
    ):
        text_splitter = SentenceTransformersTokenTextSplitter(
            chunk_overlap=chunk_overlap,
            tokens_per_chunk=tokens_per_chunk,
        )
        texts = text_splitter.split_text(context_details)
        embeddings = OllamaEmbeddings(model=embed_model_name)
        vectorstore = Chroma.from_texts(texts=texts, embedding=embeddings)

        self.retriever = vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": 5}
        )
        self.conversation_history = []
        self.model_name = model_name

    def __process_question(self, question: str, context: str) -> str:
        formatted_prompt = f"Question: {question}\n\nContext: {context}"
        response = ollama.chat(
            model=self.model_name, messages=[{'role': 'user', 'content': formatted_prompt}])
        return response['message']['content']

    def get_answer(self, question: str) -> str:
        try:
            retrieved_docs = self.retriever.invoke(question)
            formatted_context = "\n\n".join(
                doc.page_content for doc in retrieved_docs)
            if not formatted_context:
                return "No relevant context available"

            conversation_context = "\n\n".join(self.conversation_history)
            full_context = formatted_context + "\n\n" + conversation_context

            answer = self.__process_question(question, full_context)

            self.conversation_history.append(f"User: {question}")
            self.conversation_history.append(f"Bot: {answer}")

            return answer
        except Exception as e:
            print(f"\n\nError in get_answer: {e}")
            return "Sorry, there was an error processing your request."