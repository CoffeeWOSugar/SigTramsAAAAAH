import common
import wcslib as wcs
import numpy as np
from scipy import signal
import transmitter
import matplotlib.pyplot as plt

class Receiver:
    def __init__(self) -> None: ## UPPDATERA FÖR RÄTT VÄRDEN NÄR VI E KLARA MED TRANSMITTER PROBLEMEN
        self.Tb = 0.02
        self.Kc = 12
        self.OMEGAc = 2*np.pi/self.Kc
        self.fs = 48_000
        self.Ts = 1/self.fs
        self.fc = 4000
        self.wc = 8000*np.pi
        self.b_b, self.a_b = common.band_pass_filter()
        self.b_l, self.a_l = common.low_pass_filter()


    def band_limit(self, input_signal):
        output_signal = signal.lfilter(self.b_b, self.a_b, input_signal)
        return output_signal
    
    def low_pass(self, input_signal):
        return signal.lfilter(self.b_l, self.a_l, input_signal)
    
    def demodulate(self, band_limited_signal):
        k = np.arange(0, band_limited_signal.shape[0])
        yid = band_limited_signal*np.cos(k*self.OMEGAc)
        yqd = -band_limited_signal*np.sin(k*self.OMEGAc)
        yib = self.low_pass(yid)
        yqb = self.low_pass(yqd)
        return yib +1j*yqb
    
    def get_recived_data(self, yr):
        k = np.arange(0, yr.shape[0])
        plt.plot(k, yr)
        plt.savefig("4")
        plt.clf()
        ym = self.band_limit(yr)
        yb = self.demodulate(ym)
        b = wcs.decode_baseband_signal(np.abs(yb), np.angle(yb), self.Tb, self.fs)
        str = wcs.decode_string(b)
        return str
    
    def graph_test(self):
        tr = transmitter.Transmitter()
        yr = tr.graph_test()
        ym = self.band_limit(yr)
        k = np.arange(0, ym.shape[0])
        plt.plot(k, ym)
        plt.savefig("5")
        plt.clf()

        
        yb = self.demodulate(ym)
        plt.plot(k, np.abs(yb))
        plt.savefig("6.1.png")
        plt.clf()
        plt.plot(k, np.angle(yb))
        plt.savefig("6.2.png")
        plt.clf()

        b = wcs.decode_baseband_signal(np.abs(yb), np.angle(yb), self.Tb, self.fs)
        k = np.arange(0, b.shape[0])
        plt.plot(k, b)
        plt.savefig("7")
        str = wcs.decode_string(b)
        return str
    
def main():
    re = Receiver()
    print(re.graph_test())


if __name__ == "__main__":
    main()
