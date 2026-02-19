import asyncio
import json
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from kafka import KafkaConsumer
from dotenv import load_dotenv
from rag_service import rag_agent
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import ClinicalAlert

load_dotenv()

engine = create_async_engine(os.getenv("DATABASE_URL"))
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Kafka Consumer as a background task
    task = asyncio.create_task(consume_vitals())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)


async def consume_vitals():
    consumer = KafkaConsumer(
        "vitals_stream",
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    )

    print("📡 Monitoring health stream...")
    for message in consumer:
        data = message.value
        if data.get("status") == "CRITICAL":
            hr = data.get("heart_rate")
            # This calls our RAG service (Mock or Real)
            advice = await rag_agent.get_clinical_advice(hr)
            print(f"🚨 CRITICAL ALERT: HR {hr} | {advice}")

            advice = await rag_agent.get_clinical_advice(hr)

            # --- PERSISTENCE LOGIC ---
            async with AsyncSessionLocal() as session:
                async with session.begin():
                    new_alert = ClinicalAlert(
                        patient_id=data.get("patient_id"),
                        heart_rate=hr,
                        status="CRITICAL",
                        ai_advice=advice
                    )
                    session.add(new_alert)

            print(f"💾 Alert Saved to DB for HR: {hr}")

        await asyncio.sleep(0.01)


@app.get("/")
async def status():
    return {"status": "Agent Active", "mode": "Mock" if os.getenv("MOCK_AI") == "True" else "Live"}