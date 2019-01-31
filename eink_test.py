#!/usr/bin/env python3
# Copyright (c) 2019 Jarret Dyrbye
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php

from waveshare.epaper import EPaper
from waveshare.epaper import Handshake
from waveshare.epaper import RefreshAndUpdate
from waveshare.epaper import SetPallet
from waveshare.epaper import DrawRectangle
from waveshare.epaper import DrawTriangle
from waveshare.epaper import FillRectangle
from waveshare.epaper import FillTriangle
from waveshare.epaper import DisplayText
from waveshare.epaper import SetCurrentDisplayRotation
from waveshare.epaper import ReadBaudrate
from waveshare.epaper import ClearScreen

from qrdraw import QRDraw

import time
import random


SELECTIONS = [
    {'first_line':  "Coca-Cola",
     'second_line': "The Great National Temperance Beverage",
     'price':       123.33,
     'invoice':     "lnbc1233330p1pwy2sjlpp5cg2n6p2604ljsjefv3ywz0ree09m6d24vngshf9u5t0jmq3jf80sdzsgdhkxcfqgdhkccfq95s9g6r9yprhyetpwssyuct5d9hkuctvyp2x2mtsv4exzmnrv5syyetkv4exzem9cqp2rzjqfffmd5l6t4axyn0keh6lg35ls65g3m6y02snl5na53fhv8f9e8mszpg8sqqwhsqqyqqqqqfqqqqqfcqjqktpykty5j5m7n3vw926qt69fjdvrye4vzfwlquh6tvezv85q7trqmma9tnngjf570tj5975nvshlf4rdq77f2wjgdg34sf9dmt3fxxspctr0nk"},
    {'first_line':  "Pepsi Cola",
     'second_line': "You Got the Right One Baby",
     'price':       324.340,
     'invoice':     "lnbc3243400p1pwy2s48pp5zgwzlvv2ndknql8g727wetpg9wlexxsq6fhh9d6vmdc2yfylt4tqdpl2pjhqumfyppk7mrpyqkjqkt0w5sywmm5yp6xsefq2f5kw6r5yp8kuefqgfsky7gcqp2rzjqtdg6kn4nm57gsud5ctulkmpeplhy0ahd39kxudcwlgrg747j5ay7zz2wsqqzrqqqyqqqq86qqqqqqgqjq3kklhw68qdglk7kqmsnm3r484zme9k6ctuaq9449htcvzt7fvchqjx5h0ceyzryfxp0af9m5k6vk0e7wp6ntxl9krjlcpcp39mx96vgq9extkc"},
    {'first_line':  "Mountain Dew Code Red",
     'second_line': "Discover A Sensation As Real As The Streets",
     'price':       555.555,
     'invoice':     "lnbc5555550p1pwy2skkpp5eycqq2dl4twg6y0yqafpvh56chuckhp3npctw272ph7ju2df9azsdrvf4hh2mn5v95kugzyv4mjqsm0v3jjq5n9vssz6gzyd9ekxmmkv4ezqsfq2djkuumpw35k7m3qg9ejq5n9v9kzqstnyp2xsefq2d68yet9w3escqp2rzjqtdg6kn4nm57gsud5ctulkmpeplhy0ahd39kxudcwlgrg747j5ay7zz2wsqqzrqqqyqqqq86qqqqqqgqjq4fhfwjetqhg0ccpn23lss28gs8l0jqf4g3w88l7ml4679hkdzqy9m502wl5zugkqv6cqrpsh9aenrf0p4l5mzncsaa0hua8t8k86sgspamzccq"},
    {'first_line':  "Jolt Cola",
     'second_line': "All The Sugar And Twice the Caffeine",
     'price':       44.444,
     'invoice':     "lnbc444440p1pw9y5g2pp52g46yz85a65s3mnh485h03gctpum0tmx32qlke3qcna3wgvv92ysdq0ffhkcapqgdhkccgcqp2rzjqfffmd5l6t4axyn0keh6lg35ls65g3m6y02snl5na53fhv8f9e8mszpg8sqqwhsqqyqqqqqfqqqqqfcqjqxmthlx46s5rvwdf3s5y3gh7emnsvzd5xwvw8rq8jeh3c6mjsys6pewxf79svezp9pug8mm53da0yqsgf4gztdvyhnluz8jvcnz0jukqqpf38yg",
    }
]


class Screen(object):
    def __init__(self, paper):
        self.total_rectangles = 0

        self.paper = paper
        self._setup_display()

    def _handshake(self):
        print("handshake")
        h_start = time.time()
        self.paper.send(Handshake())
        print("handshake: %0.2f" % (time.time() - h_start))

    def _set_pallet(self):
        print("set pallet")
        p_start = time.time()
        self.paper.send(SetPallet(SetPallet.DARK_GRAY, SetPallet.WHITE))
        print("pallet: %0.2f" % (time.time() - p_start))

    def _set_rotation(self):
        print("set rotation")
        r_start = time.time()
        self.paper.send(
            SetCurrentDisplayRotation(SetCurrentDisplayRotation.FLIP))
        print("rotation: %0.2f" % (time.time() - r_start))


    def _setup_display(self):
        s_start = time.time()
        print("setup display")
        self._handshake()
        time.sleep(2)
        self._set_pallet()
        self._set_rotation()
        self.read_baud_rate()
        # make sure setup is acknowledged before proceeding into normal
        # operation
        self.paper.read_responses(timeout=10)
        print("finished setup in %0.2f" % (time.time() - s_start))

    def fill_rectangle(self, x1, y1, x2, y2):
        self.paper.send(FillRectangle(x1, y1, x2, y2))
        self.total_rectangles += 1

    def draw_qr(self, draw):
        d_start = time.time()
        read_count = 0
        for color, x1, y1, x2, y2 in draw.iter_draw_params(x_offset=50,
                                                           y_offset=250,
                                                           scale=6):
            if color == 0xff:
                continue
            else:
                #print("sending %d %d %d %d" % (x1, y1, x2, y2))
                self.fill_rectangle(x1, y1, x2, y2)
        print("draw qr: %0.2f" % (time.time() - d_start))

    def refresh_update(self):
        r_start = time.time()
        self.paper.send(RefreshAndUpdate())
        print("refresh update: %0.2f" % (time.time() - r_start))

    def draw_label(self, line1, line2):
        l_start = time.time()
        self.paper.send(DisplayText(10, 100, line1.encode("gb2312")))
        self.paper.send(DisplayText(10, 140, line2.encode("gb2312")))
        print("label: %0.2f" % (time.time() - l_start))

    def read_baud_rate(self):
        print("reading baud_rate")
        self.paper.send(ReadBaudrate())

    def clear_screen(self):
        print("clearing screen")
        self.paper.send(ClearScreen())

    def draw_selection(self, selection):
        d = QRDraw(selection['invoice'])
        line1 = selection['first_line']
        line2 = selection['second_line']
        d_start = time.time()
        print("drawing: %s - %s" % (line1, line2))
        self.clear_screen()
        self.draw_qr(d)
        self.draw_label(line1, line2)
        self.refresh_update()
        print("reading after: %0.2f" % (time.time() - d_start))
        self.paper.read_responses()
        print("finished: %0.2f seconds" % (time.time() - d_start))


if __name__ == '__main__':

    with EPaper() as paper:
        screen = Screen(paper)
        print("display is ready, starting in 2 seconds")
        time.sleep(2)

        for selection in SELECTIONS:
            screen.draw_selection(selection)
            print("sleeping between selections")
            time.sleep(1)

        print("any remaining?")
        b = paper.read()
        print("%d bytes remaining" % len(b))
        print("done everything")
