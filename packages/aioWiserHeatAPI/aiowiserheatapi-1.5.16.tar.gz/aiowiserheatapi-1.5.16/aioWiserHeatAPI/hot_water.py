import asyncio
import inspect
from datetime import datetime
from typing import Union

from aioWiserHeatAPI.exceptions import WiserExtraConfigError

from . import _LOGGER
from .const import (
    TEMP_HW_OFF,
    TEMP_HW_ON,
    TEMP_MINIMUM,
    TEXT_BOOST,
    TEXT_OFF,
    TEXT_ON,
    TEXT_UNKNOWN,
    WISER_BOOST_DURATION,
    WISERHOTWATER,
    WiserDeviceModeEnum,
    WiserHotWaterClimateModeEnum,
    WiserPresetOptionsEnum,
)
from .helpers.misc import is_value_in_list
from .helpers.temp import _WiserTemperatureFunctions as tf
from .rest_controller import _WiserRestController
from .schedule import _WiserSchedule


class _WiserHotwater(object):
    """Class representing a Wiser Hot Water controller"""

    def __init__(
        self,
        wiser_rest_controller: _WiserRestController,
        hw_data: dict,
        schedule: _WiserSchedule,
    ):
        self._wiser_rest_controller = wiser_rest_controller
        self._data = hw_data
        self._schedule = schedule

        self._extra_config = self._wiser_rest_controller._extra_config

        # Add device id to schedule
        if self._schedule:
            self.schedule._assignments.append({"id": self.id, "name": self.name})

    async def _send_command(self, cmd: dict):
        """
        Send control command to the hot water
        param cmd: json command structure
        return: boolen - true = success, false = failed
        """
        result = await self._wiser_rest_controller._send_command(
            WISERHOTWATER.format(self.id), cmd
        )
        if result:
            _LOGGER.debug(
                "Wiser hot water - {} command successful".format(
                    inspect.stack()[1].function
                )
            )
            return True
        return False

    @property
    def available_modes(self) -> list[str]:
        """Return available HVAC modes."""
        if self.is_climate_mode:
            return [mode.value for mode in WiserHotWaterClimateModeEnum]
        return [mode.value for mode in WiserDeviceModeEnum]

    @property
    def available_presets(self) -> list:
        """Get available preset modes"""
        # Remove advance schedule if no schedule exists or in passive mode
        if not self.schedule:
            return [
                mode.value
                for mode in WiserPresetOptionsEnum
                if mode != WiserPresetOptionsEnum.advance_schedule
            ]
        return [mode.value for mode in WiserPresetOptionsEnum]

    @property
    def away_mode_suppressed(self):
        """Get if away mode is suppressed for room"""
        return self._data.get("AwayModeSuppressed", TEXT_UNKNOWN)

    @property
    def boost_end_time(self) -> datetime:
        """Get boost end timestamp"""
        return datetime.fromtimestamp(self._data.get("OverrideTimeoutUnixTime", 0))

    @property
    def boost_time_remaining(self) -> int | float:
        """Get boost time remaining"""
        if self.is_boosted:
            return (self.boost_end_time - datetime.now()).total_seconds()
        else:
            return 0

    @property
    def current_control_source(self) -> str:
        """Get the current control source for the hot water"""
        return self._data.get("HotWaterDescription", TEXT_UNKNOWN)

    @property
    def current_state(self) -> str:
        """Get the current state of the hot water"""
        return self._data.get("HotWaterRelayState", TEXT_UNKNOWN)

    @property
    def id(self) -> int | None:
        """Get the id of the hot water channel"""
        return self._data.get("id")

    @property
    def is_away_mode(self) -> bool:
        """Return if away mode is on."""
        return (
            True if self._data.get("HotWaterDescription") == "FromAwayMode" else False
        )

    @property
    def is_boosted(self) -> bool:
        """Get if the hot water is currently boosted"""
        return True if "Boost" in self._data.get("HotWaterDescription", None) else False

    @property
    def is_climate_mode(self) -> bool:
        """Return if hw climate mode set."""
        return self._wiser_rest_controller._api_parameters.hw_climate_mode

    @property
    def is_heating(self) -> bool:
        """Get if the hot water is currently heating"""
        return True if self._data.get("WaterHeatingState") == TEXT_ON else False

    @property
    def is_override(self) -> bool:
        """Get if hotwater has an override"""
        return (
            True
            if self._data.get("OverrideType", TEXT_UNKNOWN)
            not in [TEXT_UNKNOWN, "None"]
            else False
        )

    @property
    def is_climate_mode_off(self) -> bool:
        """Determine if hw is off for climate mode."""
        if self.is_climate_mode:
            if (
                (
                    self._wiser_rest_controller._extra_config
                    and self._wiser_rest_controller._extra_config.config(
                        "HotWater", "climate_mode"
                    ).get("climate_off", False)
                )
                and self._data.get("Mode")
                in [WiserDeviceModeEnum.manual.value, WiserDeviceModeEnum.auto.value]
                and not self.is_heating
            ):
                return True

            # If not off but extr_config says it is, update extra config.
            elif self._wiser_rest_controller._extra_config:
                if self._wiser_rest_controller._extra_config.config(
                    "HotWater", "climate_mode"
                ).get("climate_off"):
                    asyncio.get_running_loop().create_task(
                        self._wiser_rest_controller._extra_config.async_update_config(
                            "HotWater", "climate_mode", {"climate_off": False}
                        )
                    )
        return False

    @property
    def mode(self) -> str | None:
        """Get or set the current hot water mode (On, Off or Auto)"""
        try:
            return TEXT_OFF if self.is_climate_mode_off else self._data.get("Mode")
        except KeyError:
            return None

    async def set_mode(
        self, mode: WiserDeviceModeEnum | WiserHotWaterClimateModeEnum | str
    ):
        """Set the hotwater mode."""
        if isinstance(mode, WiserDeviceModeEnum | WiserHotWaterClimateModeEnum):
            mode = mode.value
        if mode == WiserHotWaterClimateModeEnum.off.value:
            if self.is_climate_mode:
                await self._wiser_rest_controller._extra_config.async_update_config(
                    "HotWater", "climate_mode", {"climate_off": True}
                )
                await self._send_command(
                    {
                        "Mode": WiserDeviceModeEnum.manual.value,
                        "RequestOverride": {"Type": "None"},
                    }
                )
                await self.override_state(TEXT_OFF)
                return True
            else:
                raise ValueError(
                    f"{mode} is not a valid Hot Water mode.  Valid modes are {self.available_modes}"
                )
        elif is_value_in_list(mode, self.available_modes):
            if self.is_climate_mode:
                await self._wiser_rest_controller._extra_config.async_update_config(
                    "HotWater", "climate_mode", {"climate_off": False}
                )
            result = await self._send_command(
                {"Mode": mode.title(), "RequestOverride": {"Type": "None"}}
            )
            return result
        else:
            raise ValueError(
                f"{mode} is not a valid Hot Water mode.  Valid modes are {self.available_modes}"
            )

    @property
    def name(self) -> str:
        return "HotWater"

    @property
    def preset_mode(self) -> str | None:
        """Get the current preset mode"""
        if self.is_boosted:
            return TEXT_BOOST
        else:
            return None

    async def set_preset(self, preset: WiserPresetOptionsEnum | str):
        """Set the preset mode"""
        if isinstance(preset, WiserPresetOptionsEnum):
            preset = preset.value

        # Is it valid preset option?
        if preset in self.available_presets:
            if preset == WiserPresetOptionsEnum.cancel_overrides.value:
                await self.cancel_overrides()
            elif preset == WiserPresetOptionsEnum.advance_schedule.value:
                await self.schedule_advance()
            elif preset.lower().startswith(TEXT_BOOST.lower()):
                # Lookup boost duration
                duration = WISER_BOOST_DURATION[preset]
                _LOGGER.debug("Boosting hotwater for %s mins", duration)
                await self.override_state_for_duration("On", duration)
        else:
            raise ValueError(
                f"{preset} is not a valid preset.  Valid presets are {self.available_presets}"
            )

    @property
    def product_type(self) -> str:
        return "HotWater"

    @property
    def schedule(self) -> _WiserSchedule:
        """Get the hot water schedule"""
        return self._schedule

    @property
    def schedule_id(self):
        """Get the hot water schedule id"""
        return self._data.get("ScheduleId", 0)

    @property
    def setpoint_origin(self) -> str:
        """Get the origin of the current status for the hotwater"""
        return self._data.get("HotWaterDescription", TEXT_UNKNOWN)

    @property
    def current_target_temperature(self) -> float:
        """Return current saved target temperature if in climate mode"""
        if self.is_climate_mode:
            return (
                self._wiser_rest_controller._extra_config.config(
                    "HotWater", "climate_mode"
                ).get("target_temperature", TEMP_MINIMUM)
                if self._wiser_rest_controller._extra_config
                else TEMP_MINIMUM
            )
        return None

    async def set_target_temperature(self, temp: float) -> bool:
        """Set the target temperature of the hotwater to support climate mode."""
        if self.is_climate_mode:
            await self._wiser_rest_controller._extra_config.async_update_config(
                "HotWater", "climate_mode", {"target_temperature": temp}
            )
            return True
        raise WiserExtraConfigError(
            "You cannot set target temperature for hot water unless climate mode is not enabled."
        )

    async def boost(self, duration: int) -> bool:
        """
        Turn the hot water on for x minutes, overriding the current schedule or manual setting
        param duration: the duration to turn on for in minutes
        return: boolean
        """
        return await self.override_state_for_duration(TEXT_ON, duration)

    async def cancel_boost(self) -> bool | None:
        """
        Cancel the target temperature boost of the room
        return: boolean
        """
        if self.is_boosted:
            return await self.cancel_overrides()
        else:
            return True

    async def cancel_overrides(self):
        """
        Cancel all overrides of the hot water
        return: boolean
        """
        if self.is_override:
            return await self._send_command({"RequestOverride": {"Type": "None"}})

    async def override_state(self, state: str) -> bool:
        """
        Override hotwater state.  In auto this is until the next scheduled event.  In manual mode this is until changed.
        return: boolean
        """
        if await self.cancel_boost():
            if state.casefold() == TEXT_ON.casefold():
                return await self._send_command(
                    {
                        "RequestOverride": {
                            "Type": "Manual",
                            "SetPoint": tf._to_wiser_temp(TEMP_HW_ON, "hotwater"),
                        }
                    }
                )
            elif state.casefold() == TEXT_OFF.casefold():
                return await self._send_command(
                    {
                        "RequestOverride": {
                            "Type": "Manual",
                            "SetPoint": tf._to_wiser_temp(TEMP_HW_OFF, "hotwater"),
                        }
                    }
                )
            else:
                raise ValueError(
                    f"Invalid state value {state}.  Should be {TEXT_ON} or {TEXT_OFF}"
                )
        return False

    async def override_state_for_duration(self, state: str, duration: int) -> bool:
        """
        Override the hot water state for x minutes, overriding the current schedule or manual setting
        param duration: the duration to turn on for in minutes
        return: boolean
        """
        if state.casefold() == TEXT_ON.casefold():
            return await self._send_command(
                {
                    "RequestOverride": {
                        "Type": "Manual",
                        "DurationMinutes": duration,
                        "SetPoint": tf._to_wiser_temp(TEMP_HW_ON, "hotwater"),
                    }
                }
            )
        elif state.casefold() == TEXT_OFF.casefold():
            return await self._send_command(
                {
                    "RequestOverride": {
                        "Type": "Manual",
                        "DurationMinutes": duration,
                        "SetPoint": tf._to_wiser_temp(TEMP_HW_OFF),
                    }
                }
            )
        else:
            raise ValueError(
                f"Invalid state value {state}.  Should be {TEXT_ON} or {TEXT_OFF}"
            )

    async def schedule_advance(self) -> bool:
        """
        Advance hot water schedule to the next scheduled state setting
        return: boolean
        """
        if self.schedule:
            if await self.cancel_boost():
                return await self.override_state(self.schedule.next.setting)
        return False
