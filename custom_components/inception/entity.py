"""Base classes for Hydrawise entities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import InceptionUpdateCoordinator

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription

    from .pyinception.schema import InceptionObject


class InceptionEntity(CoordinatorEntity[InceptionUpdateCoordinator]):
    """Entity class for Inception entities."""

    _attr_has_entity_name = True
    _attr_name = None

    def __init__(
        self,
        coordinator: InceptionUpdateCoordinator,
        description: EntityDescription,
        *,
        inception_object: InceptionObject,
    ) -> None:
        """Initialize the Hydrawise entity."""
        super().__init__(coordinator=coordinator)
        self.entity_description = description
        self._attr_attribution = f"Data provided by {coordinator.api._host}"  # noqa: SLF001
        self._attr_unique_id = inception_object.ID
        self._inception_object = inception_object
        self._attr_extra_state_attributes = inception_object.extra_fields
        self._update_attrs()

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._inception_object.Name

    def _update_attrs(self) -> None:
        """Update state attributes."""
        return  # pragma: no cover

    @callback
    def _handle_coordinator_update(self) -> None:
        """Get the latest data and updates the state."""
        self._update_attrs()
        super()._handle_coordinator_update()
