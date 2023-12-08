from scipy import signal
import numpy as np

#bp = 7800pi-8200pi
#bs = 7700pi, 8300pi
#Ap, As = 0.1, 40 [db]

""" FROM DOCS https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.iirdesign.html#scipy.signal.iirdesign
Passband and stopband edge frequencies. Possible values are scalars (for lowpass and highpass filters) or ranges (for bandpass and bandstop filters).
For digital filters, these are in the same units as fs. By default, fs is 2 half-cycles/sample, so these are normalized from 0 to 1, where 1 is the Nyquist frequency.
For example:

Lowpass: wp = 0.2, ws = 0.3

Highpass: wp = 0.3, ws = 0.2

Bandpass: wp = [0.2, 0.5], ws = [0.1, 0.6]

Bandstop: wp = [0.1, 0.6], ws = [0.2, 0.5]
"""

def band_pass_filter():
    fs = 192_000
    b, a = signal.iirdesign([3900/fs, 4100/fs], [3850/fs, 4150/fs], 0.1, 40, ftype='cheby1', output='ba', fs=fs)
    return b, a


def low_pass_filter():
    fs = 192_000
    b, a = signal.iirdesign(100/fs, 7900*2/fs, 0.1, 40, ftype='butter', output='ba', fs=fs)
    return b, a
    