Note
------
STILL IN DEVELOPMENT - This is a side project I am tinkering with, so not promises for anything.

Overview
------
This library is an improvement and extension of [this repository](https://github.com/not-a-bird/waveshare-epaper-uart).  It is meant to work under Python3+ for the Raspberry Pi's GPIO output.

The API into this library is very similar to its predecessor and the provided examples there may be easily ported.

For more information about this display, see the [waveshare site](https://www.waveshare.com/4.3inch-e-paper.htm).  There is also a product [wiki page](https://www.waveshare.com/wiki/4.3inch_e-Paper_UART_Module).

It requires the GPIO library that is typically available on the Raspberry PI.

Wiring
------
This diagram is for the Pi 3, and Pi 2. This will probably work on other Raspberry Pi iterations, but double-check that the pinout is the same to be sure. [This site](https://pinout.xyz/) has a clearer visual reference for finding the pins.

| PI3 Pin  | E-Ink Pin |
|---------:|:----------|
| 3.3 v  1 | 6 3.3v    |
| GND    6 | 5 GND     |
|GPIO15 10 | 4 DOUT    |
|GPIO14  8 | 3 DIN     |
|GPIO04  7 | 2 WAKE_UP |
|GPIO02  3 | 1 RESET   |

Required Software
-----------------
The `libpython-dev` and `RPIO` libraries are needed.

    sudo apt-get install libpython-dev
    pip3 install -U RPIO

For the QR Code examples, `qrcode` will need to be installed.

    pip3 install -U qrcode

This also might need some dependencies installed via `apt-get` on the Raspberry Pi to get the binary dependencies for the QR code.

Using it
-------
Assuming everything is wired up according to the above diagram, you may still
need to disable the bluetooth serial connection (or use a different file path)
and enable the uart.

To disable the bluetooth serial connection on the Raspberry Pi 3, edit `/boot/cmdline.txt` and delete
`console=serial0,115200`.  Then edit `/boot/config.txt` and add
`dtoverlay=pi3-disable-bt` and `eanble_urar=1` and reboot.

Examples
--------

TBD
