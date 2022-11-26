"""Button support for TPLink."""
from __future__ import annotations

from kasa import SmartDevice, SmartPlug

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import TPLinkDataUpdateCoordinator
from .entity import CoordinatedTPLinkEntity, async_refresh_after


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up buttons."""
    coordinator: TPLinkDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities: list = []

    entities.append(SmartPlugReboot(coordinator.device, coordinator))

    async_add_entities(entities)


class SmartPlugReboot(CoordinatedTPLinkEntity, ButtonEntity):
    """Reboot entity of a TPLink Smart Device."""

    device: SmartPlug

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_device_class = ButtonDeviceClass.RESTART

    def __init__(
        self, device: SmartDevice, coordinator: TPLinkDataUpdateCoordinator
    ) -> None:
        """Initialize the reboot button."""
        super().__init__(device, coordinator)

        self._attr_name = f"{device.alias} Reboot"
        self._attr_unique_id = f"{self.device.mac}_device_reboot"

    @async_refresh_after
    async def async_press(self) -> None:
        """Handle the button press."""
        await self.device.reboot()
