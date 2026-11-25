# Hello world
from machine import Pin, PWM, ADC
from time import sleep_ms


class Servo:
    def __init__(self, pin):
        self.servo= PWM(Pin(pin), freq=50)      # Initialisation du PWM pour le servo

        self.T = 20                             # Période en ms
        self.t_min = 0.5                        # Durée d'impulsion minimale en ms
        self.t_max = 2.5                        # Durée d'impulsion maximale en ms

    def write(self, angle):
        # Bornage de l'angle
        angle = min(180, angle)
        angle = max(0, angle)

        # Calcul de la durée d'impulsion correspondante
        t_impulsion = self.t_min + (angle / 180) * (self.t_max - self.t_min)

        # Conversion en cycles
        cycles = int(t_impulsion / self.T * 65535)
        self.servo.duty_u16(cycles)

    def shutter(self, action):
        if action == "open":
            self.write(-60)
        elif action == "close":
            self.write(60)

class Led:
    def __init__(self, pin):
        self.led = Pin(pin, Pin.OUT)

    def on(self, duration=None):
        self.led.value(1)
        if duration is not None:
            sleep_ms(duration)
            self.off()

    def off(self):
        self.led.value(0)

class Potentiometre:
    def __init__(self, pin):
        self.potentiometre = ADC(Pin(pin))

        self.analogRead = self.potentiometre.read_u16()
        self.tensionRead = (self.potentiometre.read_u16() / 65535) * 3.3

    def update(self):
        self.analogRead = self.potentiometre.read_u16()
        self.tensionRead = (self.potentiometre.read_u16() / 65535) * 3.3

class Photoresistance:
    def __init__(self, pin, valeur_de_la_resistance, n=2.5, c=250, iso=1):
        self.photoresistance = ADC(Pin(pin))
        self.valeur_de_la_resistance = valeur_de_la_resistance
        self.n = n
        self.C = c
        self.ISO = iso

        self.analogRead = None
        self.tensionRead = None
        self.ohmRead = None
        self.luxRead = None

    def update(self):
        self.analogRead = self.photoresistance.read_u16()
        self.tensionRead = (self.analogRead / 65535) * 3.3
        self.ohmRead = self.valeur_de_la_resistance * (3.3 - self.tensionRead) / self.tensionRead
        self.luxRead = 3 * pow(10, 7) * pow(self.ohmRead, -1.4)

class Bouton:
    def __init__(self, pin):
        self.bouton = Pin(pin, Pin.IN, Pin.PULL_UP)

        self.is_pressed = not self.bouton.value()
        self.was_pressed = self.is_pressed
        self.elapsed_time = 0

def calculate_shutter_speed(lux=1000, n=2.5, c=250, iso=1):
    shutter_speed = (pow(n,2) * c) / (iso * lux) * 1000
    return shutter_speed
