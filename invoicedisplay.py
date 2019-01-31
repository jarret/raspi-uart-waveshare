#!/usr/bin/env python3
# Copyright (c) 2019 Jarret Dyrbye
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php

from waveshare.epaper import Handshake
from waveshare.epaper import RefreshAndUpdate
from waveshare.epaper import SetPallet
from waveshare.epaper import FillRectangle
from waveshare.epaper import DisplayText
from waveshare.epaper import SetCurrentDisplayRotation
from waveshare.epaper import SetEnFontSize
from waveshare.epaper import ClearScreen

from qrdraw import QRDraw

import time

class InvoiceDisplay(object):
    """
    Class for drawing soda invoices on the e-paper screen
    """
    def __init__(self, paper):
        self.paper = paper
        self._setup_display()

    def _handshake(self):
        print("handshake")
        start_time = time.time()
        self.paper.send(Handshake())
        print("handshake: %0.2f seconds" % (time.time() - start_time))

    def _set_pallet(self):
        print("set pallet")
        start_time = time.time()
        self.paper.send(SetPallet(SetPallet.DARK_GRAY, SetPallet.WHITE))
        print("set pallet: %0.2f seconds" % (time.time() - start_time))

    def _set_rotation(self):
        print("set rotation")
        start_time = time.time()
        self.paper.send(
            SetCurrentDisplayRotation(SetCurrentDisplayRotation.FLIP))
        print("set rotation: %0.2f seconds" % (time.time() - start_time))

    def _set_font_size(self):
        print("set font size")
        start_time = time.time()
        self.paper.send(SetEnFontSize(SetEnFontSize.THIRTYTWO))
        print("set font size: %0.2f seconds" % (time.time() - start_time))

    def _setup_display(self):
        start_time = time.time()
        print("setup display")
        self._handshake()
        # give the display a chance to initialize
        time.sleep(2)
        # set up specific settings
        self._set_pallet()
        self._set_rotation()
        self._set_font_size()
        # make sure setup is acknowledged before proceeding into normal
        # operation
        self.paper.read_responses(timeout=10)
        print("finished setup in %0.2f seconds" % (time.time() - start_time))

    def _fill_rectangle(self, x1, y1, x2, y2):
        self.paper.send(FillRectangle(x1, y1, x2, y2))

    def _draw_qr(self, qr_draw):
        start_time = time.time()
        read_count = 0
        for color, x1, y1, x2, y2 in qr_draw.iter_draw_params(x_offset=50,
                                                              y_offset=250,
                                                              scale=6):
            if color == 0xff:
                continue
            else:
                self._fill_rectangle(x1, y1, x2, y2)
        print("draw qr: %0.2f seconds" % (time.time() - start_time))

    def _refresh(self):
        start_time = time.time()
        self.paper.send(RefreshAndUpdate())
        print("refresh update: %0.2f seconds" % (time.time() - start_time))

    def _draw_label(self, line1, line2, price):
        start_time = time.time()
        self.paper.send(DisplayText(20, 80, line1.encode("gb2312")))
        self.paper.send(DisplayText(20, 120, line2.encode("gb2312")))
        self.paper.send(DisplayText(20, 160, price.encode("gb2312")))
        print("label: %0.2f seconds" % (time.time() - start_time))

    def _clear_screen(self):
        print("clearing screen")
        self.paper.send(ClearScreen())

    def draw_selection(self, selection):
        qd = QRDraw(selection['invoice'])
        line1 = selection['first_line']
        line2 = selection['second_line']
        price = "%.03f satoshis" % selection['price']
        start_time = time.time()
        print("drawing: %s - %s" % (line1, line2))
        self._clear_screen()
        self._draw_qr(qd)
        self._draw_label(line1, line2, price)
        self._refresh()
        print("reading after: %0.2f seconds" % (time.time() - start_time))
        self.paper.read_responses()
        print("finished: %0.2f seconds" % (time.time() - start_time))
