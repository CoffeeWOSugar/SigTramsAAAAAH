import common
import wcslib as wcs
import numpy as np
from scipy import signal
from scipy import fft
import transmitter
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf


class Receiver:
    def __init__(self) -> None: ## UPPDATERA FÖR RÄTT VÄRDEN NÄR VI E KLARA MED TRANSMITTER PROBLEMEN
        self.Tb = 0.03
        self.Kc = 8
        self.OMEGAc = 2*np.pi/self.Kc
        self.fs = 32_000
        self.Ts = 1/self.fs
        self.fc = 4000
        self.wc = 8000*np.pi
        self.b_b, self.a_b = common.band_pass_filter()
        self.b_l, self.a_l = common.low_pass_filter()
        self.is_recording = False
        self.recording = None


    def band_limit(self, input_signal):
        output_signal = signal.lfilter(self.b_b, self.a_b, input_signal)
        return output_signal
    
    def low_pass(self, input_signal):
        return signal.lfilter(self.b_l, self.a_l, input_signal)
    
    def demodulate(self, band_limited_signal):
        k = np.arange(0, band_limited_signal.shape[0])
        yid = band_limited_signal*np.cos(k*self.OMEGAc)
        yqd = -band_limited_signal*np.sin(k*self.OMEGAc)
        return yid, yqd
    
    def low_pass_IQ(self, i, q):
        yib = self.low_pass(i)
        yqb = self.low_pass(q)
        return yib + 1j*yqb

    def get_recived_data(self, yr):
        ym = self.band_limit(yr)
        yid, yqd = self.demodulate(ym)
        yb = self.low_pass_IQ(yid, yqd)
        b = wcs.decode_baseband_signal(np.abs(yb), np.angle(yb), self.Tb, self.fs)
        decoeded_str = wcs.decode_string(b)
        return decoeded_str
    
    def graph_test(self):
        tr = transmitter.Transmitter()
        yr = tr.graph_test()
        ym = self.band_limit(yr)
        k = np.arange(0, ym.shape[0])
        plt.plot(k, ym)
        plt.savefig("5")
        plt.clf()

        
        yb = self.demodulate(ym)
        #for i, e in yb:
        #    if e > 
        plt.plot(k, np.abs(yb))
        #plt.plot(k, np.abs(yb))
        plt.savefig("6.1.png")
        plt.clf()
        #plt.plot(k, np.angle(yb))
        #plt.savefig("6.2.png")
        #plt.clf()

        b = wcs.decode_baseband_signal(np.abs(yb), np.angle(yb), self.Tb, self.fs)
        k = np.arange(0, b.shape[0])
        plt.plot(k, b)
        plt.savefig("7")
        str = wcs.decode_string(b)
        print(b)
        return b

    def plot(self, name, x, y):
        plt.plot(x, y)
        plt.savefig(name + ".png")
        plt.clf()

    def record(self, time):
        rec = sd.rec(time*self.fs, samplerate=self.fs, channels=1)
        print("Recording has started")
        sd.wait()
        print("Recording has stopped")
        return rec.flatten()

    def receive_once(self):
        rec = self.record(5)

        k = np.arange(0, rec.shape[0])
        self.plot("1", k, rec)    

        ym = self.band_limit(rec)
        self.plot("2", k, ym)

        yid, yqd = self.demodulate(ym)
        self.plot("3", k, np.abs(yid + 1j*yqd))

        yb = self.low_pass_IQ(yid, yqd)
        self.plot("4.1", k, np.abs(yb))
        self.plot("4.2", k, np.angle(yb))

        b = wcs.decode_baseband_signal(np.abs(yb), np.angle(yb), self.Tb, self.fs)
        k = np.arange(0, b.shape[0])
        self.plot("5", k, b)

        str = wcs.decode_string(b)
        print(str)
        return str, False



        
def main():
    
    re = Receiver()
    #re.graph_test()
    #exit()
    with open("Recived_message.txt", "w") as f:
        txt, success = re.receive_once()
        if success:
            f.write(txt)


if __name__ == "__main__":
    main()
