#!/usr/bin/env python3
# Copyright (c) 2019 Jarret Dyrbye
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php

import RPi.GPIO as GPIO

from waveshare.epaper import EPaper

from lib.invoicedisplay import InvoiceDisplay
from lib.selections import SELECTIONS

import time


if __name__ == '__main__':
    with EPaper() as paper:
        display = InvoiceDisplay(paper)
        print("display is ready, starting in 2 seconds...")
        time.sleep(2)
        print("let's go!")

        for selection in SELECTIONS:
            display.draw_selection(selection)
            print("sleeping between selections...")
            time.sleep(1)

        print("any remaining bytes to read from the device?")
        b = paper.read()
        print("%d bytes remaining" % len(b))
        print("done everything")
