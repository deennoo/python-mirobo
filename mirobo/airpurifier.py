from .device import Device
from typing import Any, Dict
import enum


class OperationMode(enum.Enum):
    Auto = 'auto'
    Silent = 'silent'
    Favorite = 'favorite'
    Idle = 'idle'


class LedBrightness(enum.Enum):
    Bright = 0
    Dim = 1
    Off = 2


class AirPurifier(Device):
    """Main class representing the air purifier."""

    def status(self):
        """Retrieve properties."""

        # A few more properties:
        properties = ['power', 'aqi', 'humidity', 'temp_dec',
                      'mode', 'led', 'led_b', 'buzzer', 'child_lock',
                      'bright', 'favorite_level', 'filter1_life',
                      'f1_hour_used', 'use_time', 'motor1_speed']

        values = self.send(
            "get_prop",
            properties
        )
        return AirPurifierStatus(dict(zip(properties, values)))

    def on(self):
        """Power on."""
        return self.send("set_power", ["on"])

    def off(self):
        """Power off."""
        return self.send("set_power", ["off"])

    def set_mode(self, mode: OperationMode):
        """Set mode."""

        # auto, silent, favorite, idle
        return self.send("set_mode", [mode.value])

    def set_favorite_level(self, level: int):
        """Set favorite level."""

        # Set the favorite level used when the mode is `favorite`,
        # should be  between 0 and 16.
        return self.send("favorite_level", [level])  # 0 ... 16

    def set_led_brightness(self, brightness: LedBrightness):
        """Set led brightness."""

        # bright: 0, dim: 1, off: 2
        return self.send("set_led_b", [brightness.value])

    def set_led(self, led: bool):
        """Turn led on/off."""
        if led:
            return self.send("set_led", ['on'])
        else:
            return self.send("set_led", ['off'])

    def set_buzzer(self, buzzer: bool):
        """Set buzzer on/off."""
        if buzzer:
            return self.send("set_buzzer", ["on"])
        else:
            return self.send("set_buzzer", ["off"])


class AirPurifierStatus:
    """Container for status reports from the air purifier."""
    def __init__(self, data: Dict[str, Any]) -> None:
        """
        Response of a Air Purifier Pro:

        ['power': 'off', 'aqi': 41, 'humidity': 62, 'temp_dec': 293,
         'mode': 'auto', 'led': 'on', 'led_b': null, 'buzzer': null,
         'child_lock': 'off', 'limit_hum': null, 'trans_level': null,
         'bright': 71, 'favorite_level': 17, 'filter1_life': 77,
         'act_det': null, 'f1_hour_used': 771, 'use_time': 2776200,
         'motor1_speed': 0]

        Response of a Air Purifier 2:

        ['power': 'off', 'aqi': 141, 'humidity': 64, 'temp_dec': 236,
         'mode': 'auto', 'led': 'on', 'led_b': 1, 'buzzer': 'on',
         'child_lock': 'off', 'limit_hum': null, 'trans_level': null,
         'bright': null, 'favorite_level': 10, 'filter1_life': 80,
         'act_det': null, 'f1_hour_used': 680 ]

        use_time and motor1_speed is missing because a request is limitted
        to 16 properties.
        """

        self.data = data

    @property
    def power(self) -> str:
        return self.data["power"]

    @property
    def is_on(self) -> bool:
        return self.power == "on"

    @property
    def aqi(self) -> int:
        return self.data["aqi"]

    @property
    def humidity(self) -> int:
        return self.data["humidity"]

    @property
    def temperature(self) -> float:
        if self.data["temp_dec"] is not None:
            return self.data["temp_dec"] / 10.0

    @property
    def mode(self) -> OperationMode:
        return OperationMode(self.data["mode"])

    @property
    def led(self) -> bool:
        return self.data["led"] == "on"

    @property
    def led_brightness(self) -> LedBrightness:
        if self.data["led_b"] is not None:
            return LedBrightness(self.data["led_b"])

    @property
    def buzzer(self) -> bool:
        return self.data["buzzer"] == "on"

    @property
    def child_lock(self) -> bool:
        return self.data["child_lock"] == "on"

    @property
    def bright(self) -> int:
        return self.data["bright"]

    @property
    def favorite_level(self) -> int:
        # Favorite level used when the mode is `favorite`.
        return self.data["favorite_level"]

    @property
    def filter_life_remaining(self) -> int:
        return self.data["filter1_life"]

    @property
    def filter_hours_used(self) -> int:
        return self.data["f1_hour_used"]

    @property
    def use_time(self) -> int:
        return self.data["use_time"]

    @property
    def motor_speed(self) -> int:
        return self.data["motor1_speed"]

    def __str__(self) -> str:
        s = "<AirPurifierStatus power=%s, aqi=%s temperature=%s, " \
            "humidity=%s%%, mode=%s, led=%s, led_brightness=%s, buzzer=%s, " \
            "child_lock=%s, bright=%s, favorite_level=%s, " \
            "filter_life_remaining=%s, filter_hours_used=%s, " \
            "use_time=%s, motor_speed=%s>" % \
            (self.power, self.aqi, self.temperature, self.humidity, self.mode,
             self.led, self.led_brightness, self.buzzer, self.child_lock,
             self.bright, self.favorite_level, self.filter_life_remaining,
             self.filter_hours_used, self.use_time,
             self.motor_speed)
        return s
