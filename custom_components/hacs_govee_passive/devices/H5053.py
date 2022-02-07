"""Sensor platform for integration_blueprint."""
from datetime import datetime
from typing import Any

from .govee import GoveeDevice
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import TEMP_CELSIUS, PERCENTAGE

from homeassistant.helpers.entity import EntityCategory


class GoveeH5053(GoveeDevice):
    pass


class GoveeH5053_Temperature(GoveeH5053, SensorEntity):

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_native_unit_of_measurement = TEMP_CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float:
        centi_degrees_celsius = self.last_device_data["tem"]
        return centi_degrees_celsius / 100


class GoveeH5053_Humidity(GoveeH5053, SensorEntity):

    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> float:
        centi_percentage = self.last_device_data["hum"]
        return centi_percentage / 100


class GoveeH5053_Online(GoveeH5053, BinarySensorEntity):

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def is_on(self) -> bool:
        return self.available


class GoveeH5053_LastTime(GoveeH5053, SensorEntity):

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> datetime:
        return self.last_time


class GoveeH5053_Battery(GoveeH5053, SensorEntity):

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> float:
        return self.extras["deviceSettings"]["battery"]


DEVICE_SKU = "H5053"
SENSORS = [
    GoveeH5053_Temperature,
    GoveeH5053_Humidity,
    GoveeH5053_LastTime,
    GoveeH5053_Battery,
]
BINARY_SENSORS = [
    GoveeH5053_Online,
]
