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

from qrdraw import QRDraw

import time


MOCK_BOLT11 = "lnbc50n1pdm373mpp50hlcjdrcm9u3qqqs4a926g63d3t5qwyndytqjjgknskuvmd9kc2sdz2d4shyapwwpujq6twwehkjcm9ypnx7u3qxys8q6tcv4k8xtpqw4ek2ujlwd68y6twvuazqg3zyqxqzjcuvzstexcj4zcz7ldtkwz8t5pdsghauyhkdqdxccx8ts3ta023xqzwgwxuvlu9eehh97d0qcu9k5a4u2glenrekp7w9sswydl4hneyjqqzkxf54"

class Screen(object):
    def __init__(self, paper):
        self.total_read = 0
        self.total_rectangles = 0
        self.response_expected = 0

        self.paper = paper
        self._setup_display()


    def read(self, size, timeout=1):
        time.sleep(2)
        r_start = time.time()
        data = self.paper.read(size=size, timeout=timeout)
        print("read: %0.2f seconds, attempt: %d n: %d data: %s" % (
            (time.time() - r_start), size, len(data), data.hex()))
        self.total_read += len(data)
        return len(data) != 0

    def sync(self):
        print("sync")
        w_start = time.time()
        while self.read(100, timeout=2):
            pass
        print("sync: %0.2f" % (time.time() - w_start))

    def _handshake(self):
        print("handshake")
        h_start = time.time()
        self.paper.send(Handshake())
        self.read(100)
        print("handshake: %0.2f" % (time.time() - h_start))

    def _set_pallet(self):
        print("set pallet")
        p_start = time.time()
        self.paper.send(SetPallet(SetPallet.DARK_GRAY, SetPallet.WHITE))
        self.read(100)
        self.response_expected += 2
        print("pallet: %0.2f" % (time.time() - p_start))

    def _set_rotation(self):
        print("set rotation")
        r_start = time.time()
        self.paper.send(
            SetCurrentDisplayRotation(SetCurrentDisplayRotation.FLIP))
        self.read(100)
        self.response_expected += 2
        print("rotation: %0.2f" % (time.time() - r_start))

    def _setup_display(self):
        self._handshake()
        #self.sync()
        self._set_pallet()
        self._set_rotation()

    def fill_rectangle(self, x1, y1, x2, y2):
        self.paper.send(FillRectangle(x1, y1, x2, y2))
        self.total_rectangles += 1

    def draw_qr(self, draw):
        d_start = time.time()
        N_READ = 100
        read_count = 0
        for color, x1, y1, x2, y2 in draw.iter_draw_params(x_offset=100,
                                                           y_offset=300,
                                                           scale=7):
            if color == 0xff:
                continue
            else:
                #print("sending %d %d %d %d" % (x1, y1, x2, y2))
                self.fill_rectangle(x1, y1, x2, y2)

            if (read_count % N_READ) == 0:
                self.read(N_READ * 2)

            read_count += 1

        print("draw qr: %0.2f" % (time.time() - d_start))

    def refresh_update(self):
        r_start = time.time()
        self.paper.send(RefreshAndUpdate())
        self.read(100)
        print("refresh update: %0.2f" % (time.time() - r_start))

    def draw_label(self, line1, line2):
        l_start = time.time()
        self.paper.send(DisplayText(10, 100, line1.encode("gb2312")))
        self.paper.send(DisplayText(10, 140, line2.encode("gb2312")))
        self.read(100)
        print("label: %0.2f" % (time.time() - l_start))

    def read_baud_rate(self):
        self.paper.send(ReadBaudrate())
        print("reading baud_rate")
        self.read(100)
        self.response_expected += 6
        print("read baud rate")


if __name__ == '__main__':
    d = QRDraw(MOCK_BOLT11)
    line1 = "Never Gonna Give You Up!"
    line2 = "Never Gonna Let You Down!"
    print('\n'.join(d.iter_string_rows()))

    with EPaper() as paper:
        s = Screen(paper)
        s.read_baud_rate()
        s.draw_qr(d)
        s.draw_label(line1, line2)
        s.refresh_update()
        s.sync()
        print("total_read: %d" % s.total_read)
        print("total_rectangles: %d" % s.total_rectangles)

