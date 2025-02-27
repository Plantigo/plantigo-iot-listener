import json
import logging
from dataclasses import asdict

from app.core.handlers.sensors.models import TelemetryData


class SensorDataHandler:
    def __init__(self, db, redis_client):
        self.db = db
        self.redis_client = redis_client

        self.logger = logging.getLogger("SensorDataHandler")

    def handle(self, topic: str, variables: tuple, payload: str):
        try:
            mac_address = variables[0]
            telemetry = TelemetryData.from_payload(mac_address, payload)

            self.db.save(asdict(telemetry))
            self.redis_client.rpush(str(mac_address), json.dumps(asdict(telemetry)))

            self.logger.info(f"Telemetry data saved: {telemetry}")

        except ValueError as e:
            self.logger.error(f"Error processing telemetry: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
