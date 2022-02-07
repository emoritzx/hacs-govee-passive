# Govee Passive Integration

A HACS repository for Govee passive sensors

## Why?

For some reason, the Govee developer API (https://developer-api.govee.com) does not include all devices.
This integration uses a different API (https://app2.govee.com) to poll for information from passive devices,
such as temperature and humidity sensors.

There is probably a way to control active devices as well
(the same way the Govee Home Android app does),
but it is not documented.

## Supported Devices

Device | Description
------ | -----------
H5041  | Gateway
H5053  | Hygrometer Thermometer

## See also

- [LaggAt/python-govee-api](https://github.com/LaggAt/python-govee-api) for actively controlling Govee lights and switches
- [custom-components/integration_blueprint](https://github.com/custom-components/integration_blueprint) HACS integration blueprint for developing custom components
