# SPDX-FileCopyrightText: 2020-2021 Andrius Štikonas <andrius@stikonas.eu>
# SPDX-FileCopyrightText: 2021 Dave O'Connor <daveoc@google.com>
# SPDX-License-Identifier: LGPL-3.0-or-later

import logging
from datetime import datetime, timedelta
from types import SimpleNamespace

from async_property import async_property

from neohubapi.enums import HCMode
from neohubapi.enums import Weekday


class NeoStat(SimpleNamespace):
    """
    Class representing NeoStat theormostat

    Device types:
        - 12: Wired thermostat
        - 13: Wireless thermostat
        - 14: Wireless sensor
    """

    def __init__(self, hub, thermostat):
        self._logger = logging.getLogger('neohub')
        self._data_ = thermostat
        self._hub = hub

        self._simple_attrs = (
            'active_level',
            'active_profile',
            'available_modes',
            'away',
            'cool_on',
            'cool_temp',
            'current_floor_temperature',
            'date',
            'device_id',
            'device_type',
            'fan_control',
            'fan_speed',
            'floor_limit',
            'hc_mode',
            'heat_mode',
            'heat_on',
            'fan_control',
            'fan_speed',
            'hc_mode',
            'heat_mode',
            'heat_on',
            'hold_cool',
            'hold_hours',
            'hold_mins',
            'hold_off',
            'hold_on',
            'hold_state',
            'hold_temp',
            'hold_time',  # This is updated below.
            'holiday',
            'lock',
            'low_battery',
            'manual_off',
            'modelock',
            'modulation_level',
            'offline',
            'pin_number',
            'preheat_active',
            'prg_temp',
            'prg_timer',
            'sensor_mode',
            'standby',
            'stat_version',
            'switch_delay_left',  # This is updated below.
            'temporary_set_flag',
            'time',  # This is updated below.
            'timer_on',
            'window_open',
            'write_count'
        )

        for a in self._simple_attrs:
            data_attr = a.upper()
            if not hasattr(self._data_, data_attr):
                self._logger.debug(f"Thermostat object has no attribute {data_attr}")
            self.__dict__[a] = getattr(self._data_, data_attr, None)

        # Renamed attrs
        self.name = getattr(self._data_, 'ZONE_NAME', getattr(self._data_, 'device', None))
        self.target_temperature = getattr(self._data_, 'SET_TEMP', None)
        self.temperature = getattr(self._data_, 'ACTUAL_TEMP', None)

        # must be ints
        self.pin_number = int(self.pin_number)

        # HOLD_TIME can be up to 99:99
        _hold_time = list(map(int, self.hold_time.split(':')))
        _hold_time_minutes = _hold_time[0] * 60 + _hold_time[1]
        self.hold_time = timedelta(minutes=_hold_time_minutes)

        self.weekday = Weekday(self.date)

        _switch_delay_left = datetime.strptime(self.switch_delay_left, "%H:%M")
        self.switch_delay_left = timedelta(
            hours=_switch_delay_left.hour,
            minutes=_switch_delay_left.minute)

        # Wireless sensors seem to return strange time values, e.g. '255:00', so default to 00:00 instead.
        if self.device_type == 14:
            _time = datetime.strptime('00:00', "%H:%M")
            self.time = timedelta(hours=_time.hour, minutes=_time.minute)
        else:
            # The API Sometimes returns 24:XX, see https://gitlab.com/neohubapi/neohubapi/-/issues/8
            time_fragments = self.time.split(':')
            if time_fragments[0] == "24":
                corrected_time = f"00:{time_fragments[1]}"
                self._logger.debug(f"API returned {self.time} for time, correcting to {corrected_time}")
                self.time = corrected_time
            _time = datetime.strptime(self.time, "%H:%M")
            self.time = timedelta(hours=_time.hour, minutes=_time.minute)

        # 35 Degrees appears to be the hard limit in app, 5 degrees appears to be the hard lower limit.
        self.max_temperature_limit = 35
        self.min_temperature_limit = 5

        # Ensure that TIMECLOCKS are correctly reported
        if hasattr(self._data_, 'TIMECLOCK'):
            self.time_clock_mode = True
        else:
            self.time_clock_mode = False

        # Adding an attribute to deal with battery powered or not.
        if self.device_type in [2, 5, 13, 14]:
            self.battery_powered = True
        else:
            self.battery_powered = False

        if self.device_type == 1:
            # We're dealing with a NeoStat V1 there's a known bug in the API, so we must patch the hc_mode
            self.hc_mode = "HEATING"

    def __str__(self):
        """
        String representation.
        """
        data_elem = []
        for elem in dir(self):
            if not callable(getattr(self, elem)) and not elem.startswith('_'):
                data_elem.append(elem)
        out = f'HeatMiser NeoStat {self.name}:\n'
        for elem in data_elem:
            out += f' - {elem}: {getattr(self, elem)}\n'
        return out

    async def identify(self):
        """
        Flashes Devices LED light
        """

        message = {"IDENTIFY_DEV": self.name}
        reply = {"result": "Device identifying"}

        result = await self._hub._send(message, reply)
        return result

    async def rename(self, new_name):
        """
        Renames this zone
        """

        message = {"ZONE_TITLE": [self.name, new_name]}
        reply = {"result": "zone renamed"}

        result = await self._hub._send(message, reply)
        return result

    async def remove(self):
        """
        Removes this zone

        If successful, thermostat will be disconnected from the hub
        Note that it takes a few seconds to remove thermostat
        New get_zones call will still return the original list
        during that period.
        """

        message = {"REMOVE_ZONE": self.name}
        reply = {"result": "zone removed"}

        result = await self._hub._send(message, reply)
        return result

    async def set_lock(self, pin: int):
        result = await self._hub.set_lock(pin, [self])
        return result

    async def unlock(self):
        result = await self._hub.unlock([self])
        return result

    async def set_frost(self, state: bool):
        result = await self._hub.set_frost(state, [self])
        return result

    async def set_target_temperature(self, temperature: int):
        result = await self._hub.set_target_temperature(temperature, [self])
        return result

    async def set_hc_mode(self, hc_mode: HCMode):
        result = await self._hub.set_hc_mode(hc_mode, [self])
        return result

    async def set_cool_temp(self, temperature: int):
        result = await self._hub.set_cool_temp(temperature, [self])
        return result

    async def set_diff(self, switching_differential: int):
        result = await self._hub.set_diff(switching_differential, [self])
        return result

    @async_property
    async def rate_of_change(self):
        result = await self._hub.rate_of_change([self])
        roc = result[self.name]
        return roc

    async def set_timer_hold(self, state: bool, minutes: int):
        """
        Turns the output of timeclock on or off for certain duration

        Works only with NeoStats in timeclock mode
        """
        result = await self._hub.set_timer_hold(state, minutes, [self])
        return result
