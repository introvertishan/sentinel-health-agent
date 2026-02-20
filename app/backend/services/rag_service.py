import os
from dotenv import load_dotenv
from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import OllamaEmbeddings

load_dotenv()

MOCK_AI = os.getenv("MOCK_AI", "True").lower() == "true"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

class MedicalRAG:
    def __init__(self):
        if not MOCK_AI:
            self.embeddings = OllamaEmbeddings(model="llama3",base_url=OLLAMA_BASE_URL)
            self.store = PGVector(
                collection_name="medical_knowledge",
                connection_string=os.getenv("DATABASE_URL"),
                embedding_function=self.embeddings,
            )
        else:
            print("🏗️ RAG Service running in MOCK MODE.")

    async def get_clinical_advice(self, heart_rate: int):
        """Retrieves advice from Vector DB or returns a mock response."""
        if MOCK_AI:
            # Simulated delay and response
            return f"MOCK ADVICE: Patient has a heart rate of {heart_rate}. Monitor for Tachycardia. Ensure patient is resting."

        try:
            query = f"Clinical guidelines for heart rate of {heart_rate} BPM"
            docs = self.store.similarity_search(query, k=2)
            return "\n".join([doc.page_content for doc in docs])
        except Exception as e:
            return f"Error retrieving medical context: {e}"


rag_agent = MedicalRAG()