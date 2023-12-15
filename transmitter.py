import common
import wcslib as wcs
import numpy as np
import soundfile as sf
from scipy import signal
import matplotlib.pyplot as plt
import sounddevice as sd


class Transmitter:
    def __init__(self) -> None:
        self.Tb = 0.03
        self.Kc = 8
        self.OMEGAc = 2*np.pi/self.Kc
        self.fs = 32_000
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

    def do_you_enjoy_sounding(self, data):
        bits = wcs.encode_string(data)
        #bits = np.concatenate((np.zeros(8), bits))
        #bits = [False, True]
        xb = wcs.encode_baseband_signal(bits, self.Tb, self.fs)
        #xb = np.concatenate((np.zeros(self.Kc*100), xb, np.zeros(self.Kc*100)))
        
        xm = self.modulate(xb)
        xt = signal.lfilter(self.b, self.a, xm)

        #sf.write("fil.wav",xm, self.fs)
        #k = np.arange(0, 192000)
        #xt = np.zeros(192000)
        #brus_k = brus(k/self.fs)
        xt = np.concatenate((np.zeros(32000), xt, np.zeros(32000)))
        for i, e in enumerate(xt):
            xt += brus(i/self.fs)
        sf.write("fil.wav",xt, self.fs)
        #sd.play(xm, self.fs, blocking=True)


    def graph_test(self):
        bits = wcs.encode_string("cum cum cum")
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
        
def brus(k):
    return np.sin(500*2*np.pi*k)

def main():
    tr = Transmitter()
    #tr.graph_test()
    #exit()
    with open("message.txt", "r") as f:
        txt = f.read()
        txt = "Spageth monster gillar att eat bjorns spageth"
        txt = "a"
        tr.do_you_enjoy_sounding(txt)
    

if __name__ == "__main__":
    main()