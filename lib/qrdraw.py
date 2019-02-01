# Copyright (c) 2019 Jarret Dyrbye
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php

import sys
import qrcode

class QRDraw(object):
    """
    Encodes a QR code and iterates rectangle drawing instructions for
    displaying it on a pixel grid.
    """
    def __init__(self, content):
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_M,
                           box_size=1, border=2)
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

    def iter_draw_params(self, x_offset, y_offset, scale):
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

    def place_at_scale(self, x1, y1, x2, y2, cx, cy, scale):
        px1 = cx - ((self.width // 2) * scale)
        px2 = cx + ((self.width // 2) * scale)

        py1 = cy - ((self.height // 2) * scale)
        py2 = cy + ((self.height // 2) * scale)

        #print("placed %d %d to %d %d" % (px1, py1, px2, py2))

        cx = (px1 + py2) // 2
        cy = (py1 + py2) // 2

        #print("placed center point: %d %d" % (cx, cy))
        if px1 < x1:
            return None
        if py1 < y1:
            return None
        if px2 > x2:
            return None
        if py2 > y2:
            return None
        return px1, py1, px2, py2

    def place_inside_box(self, x_offset, y_offset, box_size):
        x1 = x_offset
        y1 = y_offset
        x2 = x1 + box_size
        y2 = y1 + box_size
        #print("qr native width %d" % self.width)
        #print("qr native height %d" % self.height)
        assert x2 > x1
        assert y2 > y1
        region_width = x2 - x1
        region_height = y2 - y1
        #print("region width %d" % region_width)
        #print("region height %d" % region_height)
        assert region_width == region_height

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        #print("center point: %d %d" % (cx, cy))

        last_p = None
        for scale in range(100):
            p = self.place_at_scale(x1, y1, x2, y2, cx, cy, scale)
            if not p:
                return last_p[0], last_p[1], scale - 1
            last_p = p
            scale += 1

        sys.exit("could not place code in box?)
