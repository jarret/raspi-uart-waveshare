#!/usr/bin/env python3
# Copyright (c) 2019 Jarret Dyrbye
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php

import RPi.GPIO as GPIO

from waveshare.epaper import EPaper

from invoicedisplay import InvoiceDisplay
from selections import SELECTIONS

import time


# the order of buttons to GPIO pin connection on my breadboard. YMMV
BUTTON_1 = 16
BUTTON_2 = 15
BUTTON_3 = 11
BUTTON_4 = 12

MAPPING = {BUTTON_1: SELECTIONS[0],
           BUTTON_2: SELECTIONS[1],
           BUTTON_3: SELECTIONS[2],
           BUTTON_4: SELECTIONS[3],
          }


class ButtonDrive(object):
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(BUTTON_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.display = InvoiceDisplay(EPaper(), mode=None)
        self.drawing = False

    def button(self, button_no):
        print("pressed: %d" % button_no)
        if self.drawing:
            print("drawing, skipping")
            return
        print("start draw")
        self.drawing = True
        selection = MAPPING[button_no]
        self.display.draw_selection(MAPPING[button_no])
        self.drawing = False
        print("draw finished")


if __name__ == '__main__':
    bd = ButtonDrive()
    GPIO.add_event_detect(BUTTON_1, GPIO.FALLING, callback=bd.button,
                          bouncetime=200)
    GPIO.add_event_detect(BUTTON_2, GPIO.FALLING, callback=bd.button,
                          bouncetime=200)
    GPIO.add_event_detect(BUTTON_3, GPIO.FALLING, callback=bd.button,
                          bouncetime=200)
    GPIO.add_event_detect(BUTTON_4, GPIO.FALLING, callback=bd.button,
                          bouncetime=200)
    print("start")
    while True:
        time.sleep(0.01)

    GPIO.cleanup()
