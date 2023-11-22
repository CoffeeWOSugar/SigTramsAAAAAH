import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

bp_wp = [7800*np.pi, 8200*np.pi]
bp_ws = [7700*np.pi, 8300*np.pi]

bp_Ap = 0.1
bp_As = 43

bp_Nc , bp_wn = signal.cheb1ord(bp_wp, bp_ws, bp_Ap, bp_As, analog=True)                # filter order

print(bp_Nc, bp_wn)

bp_bc, bp_ac = signal.cheby1(bp_Nc, bp_Ap, bp_wn, 'band', analog=True)                  # filter coeff

print(bp_bc, bp_ac)

bp_wc, bp_Hc = signal.freqs(bp_bc, bp_ac, worN=np.arange(7500*np.pi, 8500*np.pi, 0.1))  # freq response

plt.plot(bp_wc, 20 * np.log10(abs(bp_Hc)), label='Frequency response of bandpass filter')
plt.axvline(bp_wp[0], color='black', linestyle='--', label='Pass frequency')
plt.axvline(bp_wp[1], color='black', linestyle='--')
plt.axvline(bp_ws[0], color='red', linestyle='--', label='Stop frequency')
plt.axvline(bp_ws[1], color='red', linestyle='--')
plt.xlabel('Frequency [rad/s]')
plt.ylabel('Amplitude response [dB]')
plt.legend()
plt.grid(True)
plt.savefig("Bandpass")
plt.clf()


lp_wp = 8200*np.pi
lp_ws = 16000*np.pi

lp_Ap = 0.1
lp_As = 45 

lp_Nc, lp_wn = signal.buttord(lp_wp, lp_ws, lp_Ap, lp_As, analog=True)     # filter order

print(lp_Nc, lp_wn)

lp_bc, lp_ac = signal.butter(lp_Nc, lp_wn, analog=True)                     # filter coeff

print(lp_bc, lp_ac)

lp_wc, lp_Hc = signal.freqs(lp_bc, lp_ac, np.logspace(3, 5, 500))           # freq response

plt.plot(lp_wc, 20 * np.log10(abs(lp_Hc)), label='Frequency response of lowpass filter')
plt.axvline(8000*np.pi, color='black', linestyle='--', label='$\omega_c$')
plt.axvline(16000*np.pi, color='red', linestyle='--', label='$2\omega_c$')
plt.xscale('log')
plt.xlabel('Frequency [rad/s]')
plt.ylabel('Amplitude response [dB]')
plt.legend()
plt.grid(True)
plt.savefig("Lowpass")
plt.clf()