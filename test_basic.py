#!/usr/bin/env python3
# Copyright (c) 2019 Jarret Dyrbye
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php

import time

import RPi.GPIO as GPIO

from waveshare.epaper import EPaper
from waveshare.epaper import Handshake
from waveshare.epaper import RefreshAndUpdate
from waveshare.epaper import SetPallet
from waveshare.epaper import DrawCircle
from waveshare.epaper import FillCircle
from waveshare.epaper import DrawRectangle
from waveshare.epaper import FillRectangle
from waveshare.epaper import DrawTriangle
from waveshare.epaper import FillTriangle
from waveshare.epaper import DisplayText
from waveshare.epaper import SetCurrentDisplayRotation
from waveshare.epaper import SetEnFontSize
from waveshare.epaper import SetZhFontSize
from waveshare.epaper import ClearScreen


if __name__ == '__main__':
    with EPaper() as paper:

        paper.send(Handshake())
        time.sleep(2)
        paper.send(SetPallet(SetPallet.BLACK, SetPallet.WHITE))
        paper.send(SetCurrentDisplayRotation(SetCurrentDisplayRotation.FLIP))
        paper.send(SetEnFontSize(SetEnFontSize.THIRTYTWO))
        paper.send(SetZhFontSize(SetZhFontSize.THIRTYTWO))
        paper.read_responses(timeout=10)

        paper.send(DisplayText(20, 10, "Hello".encode("gb2312")))
        paper.send(DisplayText(20, 50, '你好'.encode("gb2312")))
        paper.send(DisplayText(20, 90, 'Здравствуйте'.encode("gb2312")))
        paper.send(DisplayText(20, 120, 'Привет'.encode("gb2312")))
        paper.send(DisplayText(20, 160, 'こんにちは'.encode("gb2312")))

        paper.send(DrawRectangle(30, 300, 60, 330))
        paper.send(FillRectangle(90, 300, 120, 330))

        paper.send(DrawTriangle(30, 400, 30, 430, 60, 430))
        paper.send(FillTriangle(90, 400, 90, 430, 120, 430))

        paper.send(DrawCircle(45, 515, 15))
        paper.send(FillCircle(105, 515, 15))

        paper.send(SetPallet(SetPallet.DARK_GRAY, SetPallet.WHITE))

        paper.send(DrawRectangle(130, 300, 160, 330))
        paper.send(FillRectangle(190, 300, 220, 330))

        paper.send(DrawTriangle(130, 400, 130, 430, 160, 430))
        paper.send(FillTriangle(190, 400, 190, 430, 220, 430))

        paper.send(DrawCircle(145, 515, 15))
        paper.send(FillCircle(205, 515, 15))

        paper.send(SetPallet(SetPallet.LIGHT_GRAY, SetPallet.WHITE))

        paper.send(DrawRectangle(230, 300, 260, 330))
        paper.send(FillRectangle(290, 300, 320, 330))

        paper.send(DrawTriangle(230, 400, 230, 430, 260, 430))
        paper.send(FillTriangle(290, 400, 290, 430, 320, 430))

        paper.send(DrawCircle(245, 515, 15))
        paper.send(FillCircle(305, 515, 15))

        paper.send(RefreshAndUpdate())
        paper.read_responses()
