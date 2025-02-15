import logging

import redis

from app.config import Config
from app.core.handlers.mqtt_handler import TelemetryHandler
from app.core.handlers.sensors.handler import SensorDataHandler
from app.db.mongodb import MongoDB
from app.mqtt.client import MQTTClient

logging.basicConfig(level=Config.LOG_LEVEL)

db = MongoDB(Config.MONGODB_URI, Config.MONGODB_DB_NAME)
mqtt_client = MQTTClient(Config.MQTT_BROKER, Config.MQTT_PORT, Config.MQTT_USERNAME, Config.MQTT_PASSWORD)
redis_client = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB)

topic_handlers = {
    "sensors/+/data": SensorDataHandler(db, redis_client),
}
handler = TelemetryHandler(db, topic_handlers)


def message_callback(client, userdata, message):
    payload = message.payload.decode()

    handler.parse_and_dispatch(message.topic, payload)


mqtt_client.connect()
mqtt_client.subscribe(list(topic_handlers.keys()))
mqtt_client.on_message(message_callback)
mqtt_client.loop_forever()
