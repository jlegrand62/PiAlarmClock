# Import GPIO Module
import RPi.GPIO as GPIO
# Import sleep Module for timing
from time import sleep

# Configures how we are describing our pin numbering
GPIO.setmode(GPIO.BOARD)  # BOARD is connector order
# Disable Warnings
GPIO.setwarnings(False)

# Set the GPIO pins that are required
OUTPUTPINS = [12, 15]
BED_PIN = 12
LIGHT_PIN = 15

def pin_activate(pin_id):
    f"""GPIO pin to activate.

    Parameters
    ----------
    pin_id : int in {OUTPUTPINS}
        Pin to activate.

    """
    GPIO.setup(pin_id, GPIO.OUT)
    return

def pin_on(pin_id):
    f"""Turn the GPIO pin to True.
    
    Parameters
    ----------
    pin_id : int in {OUTPUTPINS}
        Pin number to turn ON.

    """
    GPIO.output(pin_id, True)
    return

def pin_off(pin_id):
    f"""Turn the GPIO pin to False.
    
    Parameters
    ----------
    pin_id : int in {OUTPUTPINS}
        Pin number to turn OFF.

    """
    GPIO.output(pin_id, False)
    return

def activate_bed():
    """Run a loop that activate the pin controlling the relay module for the bed. """
    while (True):
        pin_on(BED_PIN)
        sleep(3)
        pin_off(BED_PIN)
        sleep(2)

if __name__ == '__main__':
    pin_activate(BED_PIN)
    # pin_activate(LIGHT_PIN)
    activate_bed()