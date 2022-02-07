from datetime import datetime

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

from homeassistant.helpers.entity import EntityCategory


class GoveeH5041(GoveeDevice):
    pass


class GoveeH5041_Online(GoveeH5041, BinarySensorEntity):

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def is_on(self) -> bool:
        return self.available


class GoveeH5041_LastTime(GoveeH5041, SensorEntity):

    _attr_device_class = SensorDeviceClass.TIMESTAMP
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def native_value(self) -> datetime:
        return self.last_time


DEVICE_SKU = "H5041"
SENSORS = [
    GoveeH5041_LastTime,
]
BINARY_SENSORS = [
    GoveeH5041_Online,
]
