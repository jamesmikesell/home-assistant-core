"""Binary Sensor Support for TPLink."""
from __future__ import annotations

from typing import Final, cast

from kasa import SmartDevice
from kasa.modules import Cloud

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import TPLinkDataUpdateCoordinator
from .entity import CoordinatedTPLinkEntity

CLOUD_KEY: Final = "cloud"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up binary sensors."""
    coordinator: TPLinkDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    if CLOUD_KEY not in coordinator.device.modules:
        return

    entities: list = []
    entities.append(SmartDeviceCloudConnected(coordinator.device, coordinator))
    async_add_entities(entities)


class SmartDeviceCloudConnected(CoordinatedTPLinkEntity, BinarySensorEntity):
    """Clound connection status entity of a TPLink Smart Device."""

    device: SmartDevice

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY

    def __init__(
        self, device: SmartDevice, coordinator: TPLinkDataUpdateCoordinator
    ) -> None:
        """Initialize the cloud connection binary sensor."""
        super().__init__(device, coordinator)

        self._attr_name = f"{device.alias} Cloud Connection"
        self._attr_unique_id = f"{self.device.mac}_cloud_counnection"

    @property
    def is_on(self) -> bool:
        """Return true if device is connected to cloud."""
        return cast(Cloud, self.device.modules[CLOUD_KEY]).info.cld_connection == 1
