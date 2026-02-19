import json
import time
import random
import os
from datetime import datetime
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

# Configuration from .env
KAFKA_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC_NAME = "vitals_stream"


def json_serializer(data):
    return json.dumps(data).encode("utf-8")


def get_producer():
    try:
        return KafkaProducer(
            bootstrap_servers=[KAFKA_SERVER],
            value_serializer=json_serializer,
            # Ensure the message is sent reliably
            acks='all'
        )
    except Exception as e:
        print(f"❌ Could not connect to Kafka: {e}")
        return None


def generate_vitals(patient_id="PATIENT_001"):
    """
    Simulates heart rate data.
    Most readings are normal, but 10% are 'Anomaly' events.
    """
    is_anomaly = random.random() < 0.10

    if is_anomaly:
        heart_rate = random.randint(121, 150)  # Tachycardia
        status = "CRITICAL"
    else:
        heart_rate = random.randint(65, 95)  # Normal
        status = "NORMAL"

    return {
        "patient_id": patient_id,
        "timestamp": datetime.utcnow().isoformat(),
        "heart_rate": heart_rate,
        "spo2": random.randint(94, 99),
        "status": status
    }


def run_simulator():
    producer = get_producer()
    if not producer:
        return

    print(f"🚀 Simulation started. Sending data to topic: {TOPIC_NAME}...")

    try:
        while True:
            vitals = generate_vitals()
            producer.send(TOPIC_NAME, vitals)

            print(f"📤 Sent: {vitals['heart_rate']} BPM | {vitals['status']}")

            # Wait 2 seconds between readings
            time.sleep(2)
    except KeyboardInterrupt:
        print("🛑 Simulation stopped by user.")
    finally:
        producer.close()


if __name__ == "__main__":
    run_simulator()