#!/usr/bin/env python3
# Copyright (c) 2019 Jarret Dyrbye
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php

import time

import RPi.GPIO as GPIO
from twisted.internet import reactor, threads
from twisted.internet.task import LoopingCall

from waveshare.epaper import EPaper

from lib.invoicedisplay import InvoiceDisplay
from lib.selections import SELECTIONS



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

SELECTION_MAPPING = {BUTTON_1: SELECTIONS[0],
                     BUTTON_2: SELECTIONS[1],
                     BUTTON_3: SELECTIONS[2],
                     BUTTON_4: SELECTIONS[3]}

class ButtonDrive(object):
    def __init__(self, button_event):
        self.button_event = button_event
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
        #l = MAPPING[button_no]
        #if self.state[l]:
        #    GPIO.output(l, GPIO.LOW)
        #    self.state[l] = False
        #else:
        #    GPIO.output(l, GPIO.HIGH)
        #    self.state[l] = True
        reactor.callFromThread(self.button_event, button_no)



class ButtonEInkUI(object):
    def __init__(self):
        self.bd = ButtonDrive(self.button_event)
        self.leds_on()
        paper = EPaper()
        self.display = InvoiceDisplay(paper, refresh_cb=self.refresh_cb)
        self.drawing = False
        self.blink = None
        self.led_state = None
        self.leds_off()

    def button_thread(self):
        GPIO.add_event_detect(BUTTON_1, GPIO.FALLING, callback=self.bd.button,
                              bouncetime=150)
        GPIO.add_event_detect(BUTTON_2, GPIO.FALLING, callback=self.bd.button,
                              bouncetime=150)
        GPIO.add_event_detect(BUTTON_3, GPIO.FALLING, callback=self.bd.button,
                              bouncetime=150)
        GPIO.add_event_detect(BUTTON_4, GPIO.FALLING, callback=self.bd.button,
                              bouncetime=150)

    def refresh_cb(self):
        self.blink.stop()
        self.leds_on()
        print("ok, refreshing")

    def leds_on(self):
        GPIO.output(LED_1, GPIO.HIGH)
        GPIO.output(LED_2, GPIO.HIGH)
        GPIO.output(LED_3, GPIO.HIGH)
        GPIO.output(LED_4, GPIO.HIGH)
        self.led_state = True

    def leds_off(self):
        GPIO.output(LED_1, GPIO.LOW)
        GPIO.output(LED_2, GPIO.LOW)
        GPIO.output(LED_3, GPIO.LOW)
        GPIO.output(LED_4, GPIO.LOW)
        self.led_state = False

    def leds_flip(self):
        if self.led_state:
            self.leds_off()
        else:
            self.leds_on()

    def button_event(self, button):
        if self.drawing:
            print("already drawing, dropping on floor")
            return

        print("got button: %s" % button)
        self.drawing = True
        self.leds_on()
        print("kicking off draw")
        d = threads.deferToThread(self.display.draw_selection,
                                  SELECTION_MAPPING[button])
        d.addCallback(self.finish_drawing)
        self.blink = LoopingCall(self.leds_flip)
        self.blink.start(0.2, now=False)

    def finish_drawing(self, result):
        self.drawing = False
        self.leds_off()
        print("finished_drawing")
    

if __name__ == '__main__':

    bei = ButtonEInkUI()

    reactor.callInThread(bei.button_thread)
    reactor.run()
    print("cleaning up")
    GPIO.cleanup()
