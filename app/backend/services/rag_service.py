import os
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from langchain_postgres.vectorstores import PGVector
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST")

class MedicalRAG:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="llama3")
        self.store = PGVector(
            collection_name="medical_knowledge",
            connection=os.getenv("DATABASE_URL"),
            embeddings=self.embeddings,
        )
        self.llm = OllamaLLM(model="llama3")

    async def get_clinical_advice(self, heart_rate: int):
        """Retrieves advice from Vector DB or returns a mock response."""
        try:
            query = f"Clinical guidelines for heart rate of {heart_rate} BPM"
            docs = self.store.similarity_search(query, k=2)
            context = "\n".join([doc.page_content for doc in docs])
            print("context:::::::::::::",context)
            # Combine Context + Heart Rate into a prompt for Ollama
            full_prompt = f"""
            Context: {context}

            Patient HR: {heart_rate}
            Based ONLY on the context above, provide a 1-sentence medical instruction.
            """

            response = self.llm.invoke(full_prompt)
            print("response:::::::::::::",response)
            return response

        except Exception as e:
            return f"Error retrieving medical context: {e}"


rag_agent = MedicalRAG()

# from langchain_community.vectorstores import PGVector
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain_community.llms import Ollama
# from langchain.chains import RetrievalQA
#
#
# class RAGService:
#     def __init__(self):
#         # 1. Connection string for your Postgres/PGVector
#         self.connection_string = "postgresql+psycopg2://user:pass@localhost:5432/dbname"
#         self.collection_name = "clinical_protocols"
#
#         # 2. Setup Embeddings (Must match what you used to index the data)
#         self.embeddings = OllamaEmbeddings(model="llama3")
#
#         # 3. Connect to the existing Vector Store
#         self.vectorstore = PGVector(
#             connection_string=self.connection_string,
#             collection_name=self.collection_name,
#             embedding_function=self.embeddings
#         )
#
#         # 4. Initialize Ollama
#         self.llm = Ollama(model="llama3", base_url="http://localhost:11434")
#
#     async def get_clinical_advice(self, heart_rate: int):
#         try:
#             # Create a query based on the symptoms
#             query = f"Clinical protocol for critical heart rate of {heart_rate} BPM"
#
#             # Retrieve relevant documents from PGVector
#             # 'k=2' fetches the top 2 most relevant protocol snippets
#             docs = self.vectorstore.similarity_search(query, k=2)
#             context = "\n".join([doc.page_content for doc in docs])
#
#             # Combine Context + Heart Rate into a prompt for Ollama
#             full_prompt = f"""
#             Context: {context}
#
#             Patient HR: {heart_rate}
#             Based ONLY on the context above, provide a 1-sentence medical instruction.
#             """
#
#             response = self.llm.invoke(full_prompt)
#             return response
#
#         except Exception as e:
#             return f"RAG Error: {e}"