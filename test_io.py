#!/usr/bin/env python3
# Copyright (c) 2019 Jarret Dyrbye
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php

import RPi.GPIO as GPIO

import time


# the order of buttons to GPIO pin connection on my breadboard. YMMV
BUTTON_1 = 11
BUTTON_2 = 12
BUTTON_3 = 13
BUTTON_4 = 15


LED_1 = 16
LED_2 = 18
LED_3 = 19
LED_4 = 21

MAPPING = {BUTTON_1: LED_2,
           BUTTON_2: LED_1,
           BUTTON_3: LED_3,
           BUTTON_4: LED_4}

STATE = {LED_1: None,
         LED_2: None,
         LED_3: None,
         LED_4: None}


class ButtonDrive(object):
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(BUTTON_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.setup(LED_1, GPIO.OUT)
        GPIO.setup(LED_2, GPIO.OUT)
        GPIO.setup(LED_3, GPIO.OUT)
        GPIO.setup(LED_4, GPIO.OUT)

        self.state = {LED_1: False,
                      LED_2: False,
                      LED_3: False,
                      LED_4: False}
        GPIO.output(LED_1, GPIO.LOW)
        GPIO.output(LED_2, GPIO.LOW)
        GPIO.output(LED_3, GPIO.LOW)
        GPIO.output(LED_4, GPIO.LOW)

        


    def button(self, button_no):
        print("button: %d" % button_no)
        l = MAPPING[button_no]
        if self.state[l]:
            GPIO.output(l, GPIO.LOW)
            self.state[l] = False
        else:
            GPIO.output(l, GPIO.HIGH)
            self.state[l] = True


if __name__ == '__main__':
    bd = ButtonDrive()
    GPIO.add_event_detect(BUTTON_1, GPIO.FALLING, callback=bd.button,
                          bouncetime=150)
    GPIO.add_event_detect(BUTTON_2, GPIO.FALLING, callback=bd.button,
                          bouncetime=150)
    GPIO.add_event_detect(BUTTON_3, GPIO.FALLING, callback=bd.button,
                          bouncetime=150)
    GPIO.add_event_detect(BUTTON_4, GPIO.FALLING, callback=bd.button,
                          bouncetime=150)
    print("start")
    while True:
        time.sleep(0.01)

    GPIO.cleanup()
