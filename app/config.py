import os
from app.db.utils import generate_mongo_uri


class Config:
    MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
    MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
    MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
    MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
    MQTT_TOPICS = os.getenv("MQTT_TOPICS", "").split(",") if os.getenv("MQTT_TOPICS") else []

    MONGODB_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGODB_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGODB_USER = os.getenv("MONGO_USER", "root")
    MONGODB_PASSWORD = os.getenv("MONGO_PASSWORD", "")
    MONGODB_DB_NAME = os.getenv("MONGO_DB_NAME", "iot_database")

    MONGODB_URI = generate_mongo_uri(
        MONGODB_HOST, MONGODB_PORT, MONGODB_USER, MONGODB_PASSWORD
    ) if MONGODB_HOST else None

    MONGODB_MAX_CONNECTIONS = int(os.getenv("MONGO_MAX_CONNECTIONS", 10))

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

    REDIS_URI = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    if REDIS_PASSWORD:
        REDIS_URI = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"