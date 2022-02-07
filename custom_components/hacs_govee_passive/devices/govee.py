"""Sensor platform for integration_blueprint."""
from datetime import datetime
import json
from typing import Any
from homeassistant.helpers.update_coordinator import CoordinatorEntity
import pytz
from ..const import DOMAIN


class GoveeDevice(CoordinatorEntity):
    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id

    @property
    def data(self) -> dict[str, Any]:
        return next(
            filter(
                lambda device: device["device"] == self.device_id, self.coordinator.data
            )
        )

    @property
    def extras(self) -> dict[str, Any]:
        extras: dict[str, Any] = self.data["deviceExt"]
        return {k: json.loads(v) for k, v in extras.items()}

    @property
    def last_device_data(self) -> dict[str, Any]:
        return self.extras["lastDeviceData"]

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self.device_id)},
            "name": self.data["deviceName"],
            "manufacturer": "Govee",
            "model": self.data["sku"],
            "via_device": (DOMAIN, "Govee API (cloud)"),
        }

    @property
    def name(self) -> str:
        name = self.data["deviceName"]
        return f"{name} {self.device_class}"

    @property
    def available(self) -> bool:
        return self.last_device_data["online"]

    @property
    def last_time(self) -> datetime:
        timestamp_seconds = self.last_device_data["lastTime"] / 1000
        return datetime.fromtimestamp(timestamp_seconds, pytz.utc)

    @property
    def unique_id(self) -> str:
        return f"{self.device_id}-{self.device_class}"
