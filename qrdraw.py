# Copyright (c) 2019 Jarret Dyrbye
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php

import qrcode

class QRDraw(object):
    """
    Encodes a QR code and iterates rectangle drawing instructions for
    displaying it on a pixel grid.
    """
    def __init__(self, content):
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_M,
                           box_size=1, border=0)
        qr.add_data(content)
        img = qr.make_image(fill_color="black", back_color="white")
        l = img.convert("L")
        self.width, self.height = l.size
        d = l.getdata()
        self.data = bytearray(d)

    def iter_rows(self):
        for y in range(self.height):
            yield y, self.data[y * self.width:y * self.width + self.width]

    def iter_rects(self):
        for y, row in self.iter_rows():
            x_start = 0
            color = row[0]
            for x in range(len(row)):
                if row[x] == color:
                    continue
                else:
                    x_end = x
                    yield y, x_start, x_end, row[x_start:x_end]
                    x_start = x
                    color = row[x]
            x_end = len(row)
            yield y, x_start, x_end, row[x_start:x_end]

    def iter_string_rows(self):
        rows = {}
        for y, x_start, x_end, rect in self.iter_rects():
            if y not in rows.keys():
                rows[y] = []
            s = ""
            for b in rect:
                s += "1" if b == 0x00 else "."
            rows[y].append({'y':     y,
                            'start': x_start,
                            'end':   x_end,
                            'data':  rect,
                            'str':   s})
        for rects in rows.values():
            yield "".join(rect['str'] for rect in rects)

    def iter_draw_params(self, x_offset=30, y_offset=30, scale=2):
        for y, x_start, x_end, rect in self.iter_rects():
            x_start = x_start * scale
            x_end = (x_end * scale) - 1
            y_start = (y * scale)
            y_end = ((y + 1) * scale) - 1
            color = rect[0]
            #print("%s, y: %d xstart: %d xend: %d" % (rect, y, x_start, x_end))
            y1 = y_start + y_offset
            y2 = y_end + y_offset
            x1 = x_start + x_offset
            x2 = x_end + x_offset
            yield color, x1, y1, x2, y2
