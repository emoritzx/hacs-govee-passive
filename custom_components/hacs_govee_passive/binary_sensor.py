from .devices import DEVICES
from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    for device_type in DEVICES:
        for device_data in filter(
            lambda device: device["sku"] == device_type.DEVICE_SKU, coordinator.data
        ):
            entities = []
            for entity in device_type.BINARY_SENSORS:
                entities.append(entity(coordinator, device_data["device"]))
            async_add_devices(entities)
