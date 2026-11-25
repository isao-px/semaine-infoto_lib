# semaine_infoto

Bibliothèque **MicroPython** pour Arduino à base d'**ESP32** (p. ex. Nano ESP32), destinée à piloter un obturateur d'appareil photo.

Elle utilise le module `machine` du firmware MicroPython : elle ne fonctionne pas avec Python sur un ordinateur.

## Installation sur la carte

`mip`, le gestionnaire de paquets de MicroPython, n'utilise pas PyPI. Il faut donc télécharger le paquet sur l'ordinateur, puis le copier sur la carte :

```sh
pip install mpremote
pip install --no-compile --target lib_carte semaine_infoto
mpremote fs mkdir :lib
mpremote fs cp -r lib_carte/semaine_infoto :lib/
```

Si `:lib` existe déjà, ignorer l'erreur de `mkdir`.

Depuis une copie locale du dépôt, dans le dossier de la bibliothèque, `mpremote mip install package.json` suffit.

## Utilisation

```python
from semaine_infoto import Led, Photoresistance, Servo, calculate_shutter_speed

led = Led(8)
servo = Servo(9)
capteur = Photoresistance("A6", 10000)

capteur.update()
temps_ms = calculate_shutter_speed(lux=capteur.luxRead, n=2.5, c=250, iso=1)
led.on(duration=500)
servo.write(60)
```

## Contenu

| Élément | Rôle |
|---|---|
| `Servo(pin)` | `write(angle)` (0 à 180°), `shutter("open" / "close")` |
| `Led(pin)` | `on(duration=None)` (durée en ms, bloquant), `off()` |
| `Potentiometre(pin)` | `update()`, puis `analogRead`, `tensionRead` |
| `Photoresistance(pin, valeur_de_la_resistance)` | `update()`, puis `analogRead`, `tensionRead`, `ohmRead`, `luxRead` |
| `Bouton(pin)` | `is_pressed`, `was_pressed`, `elapsed_time` |
| `calculate_shutter_speed(lux, n, c, iso)` | Temps de pose en ms |

## Tests

Sur l'ordinateur, avec un faux module `machine` :

```sh
python -m unittest discover -s tests
```

## Licence

MIT, voir le fichier `LICENSE`.
