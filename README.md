# 🩺 Sentinel Health Agent: Autonomous Clinical RAG Pipeline

[![CI Quality Check](https://github.com/YOUR_USERNAME/sentinel-health-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/sentinel-health-agent/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

An autonomous, event-driven healthcare monitoring system designed for elderly care. This project moves beyond simple threshold alerts by using **Retrieval-Augmented Generation (RAG)** to provide medically-grounded clinical decision support in real-time.

---

## 🏗️ System Architecture

The system follows a distributed "Logic Node" architecture, separating data ingestion, clinical reasoning, and user interaction.



### **Core Workflow**
1.  **Ingestion:** A custom simulation engine streams physiological data (HR, SpO2) into **Apache Kafka**.
2.  **Detection:** A **FastAPI** consumer monitors the stream. If a vital sign exceeds a deterministic threshold, an "Alert State" is triggered.
3.  **Contextual Retrieval:** The system performs a semantic search in **PostgreSQL (pgvector)** to find relevant medical guidelines and fetches the patient's structured medical history.
4.  **Reasoning:** Local **Ollama (Llama 3)** synthesizes the vitals, history, and guidelines to generate a personalized clinical recommendation.
5.  **Visualization:** Real-time metrics and AI reasoning are displayed on a **Streamlit** dashboard.

---

## 🛠️ Tech Stack

* **Backend:** FastAPI (Asynchronous logic node)
* **Message Broker:** Apache Kafka (Real-time telemetry)
* **Database:** PostgreSQL with `pgvector` (Structured history + Unstructured medical embeddings)
* **AI/LLM:** Ollama (Llama 3 for inference, `mxbai-embed-large` for embeddings)
* **Orchestration:** LangChain (RAG pipeline management)
* **Security:** OAuth 2.0 + JWT (Stateless authentication)
* **Frontend:** Streamlit (Real-time monitoring dashboard)
* **DevOps:** GitHub Actions (CI), Pre-commit hooks (Ruff, Mypy)

---

## 🚀 Senior-Level Features

-   **Deterministic-Probabilistic Hybrid:** Combines reliable `if-this-then-that` alerting with nuanced LLM clinical reasoning.
-   **Stateless Security:** Implements industry-standard OAuth 2.0 flow with JWT tokens to secure sensitive health endpoints.
-   **Synthetic Data Generation:** Includes a specialized simulation engine to stress-test the pipeline without PII/HIPAA constraints.
-   **Scalable Event-Driven Design:** Uses Kafka to decouple data ingestion from clinical logic, allowing for horizontal scaling.

---

## 📥 Getting Started

### **Prerequisites**
- Docker & Docker Compose
- Conda or Python 3.11+
- [Ollama](https://ollama.com/) installed and running locally

### **Installation**
1. **Clone & Setup Environment:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/sentinel-health-agent.git](https://github.com/YOUR_USERNAME/sentinel-health-agent.git)
   cd sentinel-health-agent
   conda create -n health-agent python=3.11
   conda activate health-agent
   pip install -r requirements.txt
2. **Spin up Infrastructure:**
    ```bash
   docker-compose up -d
3. **Prepare the AI:**
    ```bash
   ollama pull llama3
   ollama pull mxbai-embed-large
4. **Setup Database:**
    ```bash
   python init_db.py
   