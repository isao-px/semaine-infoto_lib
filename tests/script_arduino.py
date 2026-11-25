# Hello world
from machine import Pin, PWM, ADC
from classes import Servo, Led, Potentiometre, Bouton, Photoresistance, calculate_shutter_speed
from time import ticks_ms, sleep_ms

# Définition des constantes matérielles
VALEUR_DE_LA_RESISTANCE = 10000                     # Valeur de la résistance de la photoresistance
CIRCUIT_PHOTORESISTANCE_PIN = "A6"                  # Pin du circuit de la photoresistance
BOUTON_PIN = 3                                      # Pin du bouton
LED_PIN = 8                                         # Pin de la LED
SERVO_PIN = 9                                       # Pin du servo-moteur
POTENTIOMETRE_PIN = "A3"                            # Pin du potentiomètre

# Constantes et variables de l'appareil
SHUTTER_SPEED_MIN = 200                             # Vitesse d'obturation minimale (constante)
ISO = 1                                             # Sensibilité du papier (constante)
C = 250                                             # Constante du luxmètre
n = 2.5                                             # Valeur de l'ouverture (variable)
F = 100                                             # Valeur de la focale (constante)
diametre_ouverture = 0.0                            # Diamètre de l'ouverture (variable)
shutter_is_open = False                             # État de l'obturateur (variable)
blob_is_on = False                                  # État du mode blob (variable)

# Initialisation
servo = Servo(SERVO_PIN)                            # Instance de la classe Servo
servo.write(60)                                     # Homing de l'obturateur
led = Led(LED_PIN)                                  # Instance de la classe Led
potentiometre = Potentiometre(POTENTIOMETRE_PIN)    # Instance de la classe Potentiometre
bouton = Bouton(BOUTON_PIN)                         # Instance de la classe Bouton
                                                    # Instance de la classe Photoresistance
photoresistance = Photoresistance(CIRCUIT_PHOTORESISTANCE_PIN, VALEUR_DE_LA_RESISTANCE)

##### MAIN #####

while True:
    # MàJ des mesures
    potentiometre.update()
    photoresistance.update()
    shutter_speed = calculate_shutter_speed(
        lux = photoresistance.luxRead,
        n = n,
        c = C,
        iso = ISO
    )

    # En cas de front montant (bouton pressé) :
    if bouton.is_pressed and not bouton.was_pressed and not shutter_is_open:
        bouton.elapsed_time = ticks_ms()

        if shutter_speed < SHUTTER_SPEED_MIN:
            led.on(duration=500)
        else:
            servo.shutter("open")
            shutter_is_open = True

    # Si les conditions pour le mode blob sont remplies :
    if bouton.elapsed_time > 500 and bouton.is_pressed and bouton.was_pressed:
        if not shutter_is_open:
            servo.shutter("open")
            shutter_is_open = True
        blob_is_on = True

    # Si une exposition est en cours, que le temps d'exposition est écoulé et que le blob n'est pas actif :
    if shutter_is_open and (ticks_ms() - bouton.elapsed_time) >= shutter_speed and not blob_is_on:
        servo.shutter("close")
        shutter_is_open = False

    # En cas de front descendant (bouton relâché) :
    if not bouton.is_pressed and bouton.was_pressed:
        if blob_is_on:
            servo.shutter("close")
            shutter_is_open = False
            blob_is_on = False

    # MàJ de l'état du bouton et temporisation
    bouton.was_pressed = bouton.is_pressed
    sleep_ms(5)