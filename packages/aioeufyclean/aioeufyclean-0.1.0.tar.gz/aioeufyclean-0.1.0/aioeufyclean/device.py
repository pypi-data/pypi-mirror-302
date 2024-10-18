# Copyright 2019 Richard Mitchell
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import json
import logging
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from .tuya import TuyaDevice

_LOGGER = logging.getLogger(__name__)


class WorkMode(StrEnum):
    AUTO = "auto"
    NO_SWEEP = "Nosweep"
    SMALL_ROOM = "SmallRoom"
    EDGE = "Edge"
    SPOT = "Spot"


class Direction(StrEnum):
    LEFT = "left"
    RIGHT = "right"
    FORWARD = "forward"
    BACKWARD = "backward"


class CleanSpeed(StrEnum):
    NO_SUCTION = "No_suction"
    STANDARD = "Standard"
    BOOST_IQ = "Boost_IQ"
    MAX = "Max"


class ErrorCode(StrEnum):
    NO_ERROR = "no_error"
    WHEEL_STUCK = "Wheel_stuck"
    R_BRUSH_STUCK = "R_brush_stuck"
    CRASH_BAR_STUCK = "Crash_bar_stuck"
    SENSOR_DIRTY = "sensor_dirty"
    NOT_ENOUGH_POWER = "N_enough_pow"
    STUCK_5_MIN = "Stuck_5_min"
    FAN_STUCK = "Fan_stuck"
    S_BRUSH_STUCK = "S_brush_stuck"


class State(StrEnum):
    DOCKED = "docked"
    CLEANING = "cleaning"
    RETURNING = "returning"
    ERROR = "error"
    PAUSED = "paused"
    ON = "on"
    OFF = "off"
    IDLE = "idle"


class BinarySensor(StrEnum):
    pass


class Sensor(StrEnum):
    BATTERY = "battery"
    FILTER_LIFE = "filter_life"
    SIDE_BRUSH_LIFE = "side_brush_life"
    ROLLING_BRUSH_LIFE = "rolling_brush_life"
    SENSOR_CLEAN_LIFE = "sensor_clean_life"


@dataclass
class VacuumState:
    state: State
    sensors: dict[Sensor, str | int | float]
    binary_sensors: dict[BinarySensor, bool]


class VacuumDevice(TuyaDevice):
    """Represents a generic Eufy Robovac."""

    POWER = "1"
    PLAY_PAUSE = "2"
    DIRECTION = "3"
    WORK_MODE = "5"
    WORK_STATUS = "15"
    GO_HOME = "101"
    CLEAN_SPEED = "102"
    FIND_ROBOT = "103"
    BATTERY_LEVEL = "104"
    ERROR_CODE = "106"
    CONSUMABLE = "116"

    def _handle_state_update(self, payload: dict[str, Any]) -> VacuumState:
        if payload.get(self.ERROR_CODE) != 0:
            state = State.ERROR
        elif payload.get(self.POWER) == "1" or payload.get(self.WORK_STATUS) in (
            "Charging",
            "completed",
        ):
            state = State.DOCKED
        elif payload.get(self.WORK_STATUS) in ("Recharge",):
            state = State.RETURNING
        elif payload.get(self.WORK_STATUS) in ("Sleeping", "standby"):
            state = State.IDLE
        else:
            state = State.CLEANING

        vacuum_state = VacuumState(
            state=state,
            sensors={},
            binary_sensors={},
        )

        if self.BATTERY_LEVEL in payload:
            vacuum_state.sensors[Sensor.BATTERY] = payload[self.BATTERY_LEVEL]

        if consumable_json := payload.get(self.CONSUMABLE):
            if (
                duration := json.loads(base64.b64decode(consumable_json))
                .get("consumable", {})
                .get("duration", {})
            ):
                # TODO: What are SP, TR and BatteryStatus?
                if "FM" in duration:
                    vacuum_state.sensors[Sensor.FILTER_LIFE] = duration["FM"]
                if "RB" in duration:
                    vacuum_state.sensors[Sensor.ROLLING_BRUSH_LIFE] = duration["RB"]
                if "SB" in duration:
                    vacuum_state.sensors[Sensor.SIDE_BRUSH_LIFE] = duration["SB"]
                if "SS" in duration:
                    vacuum_state.sensors[Sensor.SENSOR_CLEAN_LIFE] = duration["SS"]

        return vacuum_state

    async def async_start(self) -> None:
        await self.async_set({self.WORK_MODE: str(WorkMode.AUTO)})

    async def async_pause(self) -> None:
        await self.async_set({self.PLAY_PAUSE: False})

    async def async_stop(self) -> None:
        await self.async_set({self.PLAY_PAUSE: False})

    async def async_return_to_base(self) -> None:
        await self.async_set({self.GO_HOME: True})

    async def async_locate(self) -> None:
        await self.async_set({self.FIND_ROBOT: True})

    async def async_set_fan_speed(self, clean_speed: CleanSpeed) -> None:
        await self.async_set({self.CLEAN_SPEED: str(clean_speed)})
