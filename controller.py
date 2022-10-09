
from machine import Pin

key0 = Pin(15,Pin.IN)
key1 = Pin(17,Pin.IN)
key2 = Pin(2 ,Pin.IN)
key3 = Pin(3 ,Pin.IN)
pressed = False

def button_pressed():
    global pressed
    if(key0.value() == 0 or key1.value() == 0 or key2.value() == 0 or key3.value() == 0):
        if pressed is False:
            pressed = True
            return True
        return False
    else :
        pressed = False
        return False

