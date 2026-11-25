"""Tests exécutés sur PC (CPython) : le matériel MicroPython est simulé."""
import sys
import time
import unittest
from pathlib import Path
from unittest.mock import MagicMock

sys.modules["machine"] = MagicMock()
time.sleep_ms = MagicMock()
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import semaine_infoto as si


class TestSemaineInfoto(unittest.TestCase):
    def test_servo_borne_angle(self):
        servo = si.Servo(9)
        for angle, cycles in ((-10, 1638), (0, 1638), (180, 8191), (200, 8191)):
            servo.write(angle)
            servo.servo.duty_u16.assert_called_with(cycles)

    def test_led_duree(self):
        led = si.Led(8)
        led.led.reset_mock()
        led.on(duration=500)
        time.sleep_ms.assert_called_with(500)
        self.assertEqual([c.args[0] for c in led.led.value.call_args_list], [1, 0])

    def test_photoresistance(self):
        capteur = si.Photoresistance("A6", 10000)
        capteur.photoresistance.read_u16.return_value = 32768
        capteur.update()
        self.assertAlmostEqual(capteur.ohmRead, 10000, delta=1)

    def test_temps_de_pose(self):
        self.assertAlmostEqual(si.calculate_shutter_speed(1000, 2.5, 250, 1), 1562.5)


if __name__ == "__main__":
    unittest.main()
