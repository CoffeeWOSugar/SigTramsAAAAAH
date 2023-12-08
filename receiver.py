import common
import wcslib as wcs
import numpy as np
from scipy import signal

class Receiver:
    def __init__(self) -> None:
        self.Tb = 0.02
        self.Kc = 48
        self.fs = 192_000
        self.Ts = 1/self.fs
        self.fc = 4000
        self.wc = 8000*np.pi
        self.b_b, self.a_b = common.band_pass_filter()
        self.b_l, self.a_l = common.low_pass_filter()


    def band_limit(self, input_signal):
        output_signal = signal.lfilter(self.b_b, self.a_b, input_signal)
        return output_signal
    def demodulate(self):
        
        return 0
    def decode(self):
        return 0
    

