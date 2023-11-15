import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

w_start = 7999.9* np.pi
delta_w = 0.001
w_stop = 8000 * np.pi
w_arr = np.arange(w_start, w_stop, delta_w)

wc = 8000 * np.pi
Tb = 1/50
Ac = np.sqrt(2) # SET TO SOMETHING BETTER IN 1c
bn = 1

def signal(w, i):
    res = 0
    res += 1 * np.e**(-1j*w*(i*0.5))
    return res
    

def Xb(w,i):
    return Tb * signal(w,i)
    return Tb * np.sinc(w*Tb/(2*np.pi)) * signal(w)

def Xm(w,i):
    return np.abs(((Ac*1j)/2)*(Xb(w + wc,i) - Xb(w - wc,i)))


#print(len(w_arr))
#np.array([Xm(w) for w in w_arr])
for j in [1, 10]:
    print(j)
    result = np.zeros(len(w_arr), dtype="float128")
    for i,w in enumerate(w_arr):
        result[i] = Xm(w,j)
    plt.plot(w_arr, result, label="Xm(w)")

# Give x, y, title axis label 
plt.ylabel('x(t)') 
plt.xlabel('omega [rad / s]') 
#plt.axhline(0, color='blue', label='$x_{even}$')
#plt.axvline(0,color='grey')
plt.legend()
  
# Display 
plt.show()