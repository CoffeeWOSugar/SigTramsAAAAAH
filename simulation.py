#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulation template for the wireless communication system project in Signals 
and Transforms.

For plain text inputs, run:
$ python3 simulation.py "Hello World!"

For binary inputs, run:
$ python3 simulation.py -b 010010000110100100100001

2020-present -- Roland Hostettler <roland.hostettler@angstrom.uu.se>
"""

import sys
import numpy as np
from scipy import signal
#import matplotlib.pyplot as plt
import wcslib as wcs
import transmitter
import receiver


# \frac{At}{2}\frac{\sin\left(xt-2\pi\right)}{xt-2\pi}+\frac{At}{2}\frac{\sin\left(xt+2\pi\right)}{xt+2\pi}

def main():
    # Parameters
    # TODO: Add your parameters here. You might need to add other parameters as 
    # well.
    channel_id = 15      # Your channel ID
    Tb = 0.03            # Symbol width in seconds
    fs = 32_000           # Sampling frequency in Hz

    # Detect input or set defaults
    string_data = True
    if len(sys.argv) == 2:
        data = str(sys.argv[1])

    elif len(sys.argv) == 3 and str(sys.argv[1]) == '-b':
        string_data = False
        data = str(sys.argv[2])

    elif len(sys.argv) == 6:
        channel_id = str(sys.argv[3])
        Tb = str(sys.argv[4])
        fs = str(sys.argv[5])

    else:
        print('Warning: No input arguments, using defaults.', file=sys.stderr)
        data = "Test"

    # Convert string to bit sequence or string bit sequence to numeric bit
    # sequence
    if string_data:
        bs = wcs.encode_string(data)
    else:
        bs = np.array([bit for bit in map(int, data)])

    # Encode baseband signal
    xb = wcs.encode_baseband_signal(bs, Tb, fs)

    # TODO: Put your transmitter code here (feel free to modify any other parts
    # too, of course)

    trans = transmitter.Transmitter()
    xt = trans.get_transmit_signal(xb)
    
    # Channel simulation
    # TODO: Enable channel simulation.
    yr = wcs.simulate_channel(xt, fs, channel_id)

    # TODO: Put your receiver code here. Replace the three lines below, they
    # are only there for illustration and as an MWE. Feel free to modify any
    # other parts of the code as you see fit, of course.
    #yb = xb*np.exp(1j*np.pi/5) + 0.1*np.random.randn(xb.shape[0])
    #ybm = np.abs(yb)
    #ybp = np.angle(yb)
    #viktig kommentar
    rec = receiver.Receiver()
    print(rec.get_recived_data(yr))


    # Baseband and string decoding
    #br = wcs.decode_baseband_signal(ybm, ybp, Tb, fs)
    #data_rx = wcs.decode_string(br)
    #print('Received: ' + data_rx)


if __name__ == "__main__":
    main()
