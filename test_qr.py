#!/usr/bin/env python3
# Copyright (c) 2019 Jarret Dyrbye
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php

import time

from lib.qrdraw import QRDraw
from lib.selections import SELECTIONS

bolt11 = SELECTIONS[1]['invoice']


qd = QRDraw(bolt11)

for r in qd.iter_string_rows():
    print(r)


x_offset, y_offset, scale = qd.place_inside_box(0, 0, 100)

for color, x1, y1, x2, y2 in qd.iter_draw_params(x_offset, y_offset, scale):
    print("%d %d %d %d %d" % (x1, y1, x2, y2, color))
