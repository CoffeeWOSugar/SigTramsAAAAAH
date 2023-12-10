import common
import wcslib as wcs
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

class Transmitter:
    def __init__(self) -> None:
        self.Tb = 0.02
        self.Kc = 12
        self.OMEGAc = 2*np.pi/self.Kc
        self.fs = 48_000
        self.Ts = 1/self.fs
        self.fc = 4000
        self.wc = 8000*np.pi
        self.b, self.a = common.band_pass_filter()
        self.Ac = np.sqrt(2)
    
    def get_transmit_signal(self, xb):
        lst = xb.tolist()
        lst = [0 for _ in range(self.Kc*100)] + lst + [0 for _ in range(self.Kc*100)]
        xb = np.array(lst)
        xm = self.modulate(xb)
        xt = signal.lfilter(self.b, self.a, xm)
        return xt

    def modulate(self, xb):
        k = np.arange(0, xb.shape[0])
        xc = self.Ac*np.sin(k*self.OMEGAc)
        return xc*xb

    def graph_test(self):
        bits = wcs.encode_string("Absolut vodka")
        k = np.arange(0, bits.shape[0])
        plt.plot(k, bits)
        plt.savefig("1")
        plt.clf()
        xb = wcs.encode_baseband_signal(bits, self.Tb, self.fs)
        lst = xb.tolist()
        lst = [0 for _ in range(self.Kc*100)] + lst + [0 for _ in range(self.Kc*100)]
        xb = np.array(lst)
        k = np.arange(0, xb.shape[0])
        plt.plot(k, xb)
        plt.savefig("2")
        plt.clf()
        xm = self.modulate(xb)
        plt.plot(k, xm)
        plt.savefig("3")
        plt.clf()
        xt = signal.lfilter(self.b, self.a, xm)
        plt.plot(k, xt)
        plt.savefig("4")
        plt.clf()
        return xt
        


def main():
    tr = Transmitter()
    tr.graph_test()

if __name__ == "__main__":
    main()