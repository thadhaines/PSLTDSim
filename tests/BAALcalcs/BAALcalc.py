""" Equations use to calculate BAAL via BAL-001-2 R2"""
import numpy as np
import matplotlib.pyplot as plt

# all about keeping RACE within BAAL limits at least once within a 30 minute window...
Fbase = 60
Fs = 1*Fbase

Beta = -100 # frequency bias
Fa = 60.005 # actual frequency - rolling minute average...

eps1 = 0.0228 # Hz, dictated by interconnection

FTL_low = Fs - 3*eps1 # frequency trigger limit
FTL_high = Fs + 3*eps1
f_dev_High = FTL_high - Fs
f_dev_Low = FTL_low - Fs

f_dev = Fa-Fs

# if Fs= Fa, BAAL does not apply...?
BAAL_low = -10*Beta*f_dev_Low*(f_dev_Low/f_dev)
BAAL_high = -10*Beta*f_dev_High*(f_dev_High/f_dev)



fRangeL = np.arange(59.96, 59.999, 0.001)
fRangeH = np.arange(60.001, 60.04, 0.001)
fRange = np.concatenate((fRangeL , fRangeH), axis=0)
BAAL_range = np.zeros_like(fRange)
n = 0

for f in fRange:
    f_dev = f-Fs

    if f_dev > 0:
        #print(str(f)+' BAAL high = %.2f' % BAAL_high)
        BAAL_range[n]= -10*Beta*f_dev_High*(f_dev_High/f_dev)
    elif f_dev < 0:
        #print(str(f)+' use BAAL Low = %.2f' % BAAL_low)
        BAAL_range[n]= -10*Beta*f_dev_Low*(f_dev_Low/f_dev)
    elif f_dev == 0.0:
        #print('Frequency match, BAAL does not apply')
        BAAL_range[n]= 0

    n += 1

fig, ax = plt.subplots()
# Testing of output (i.e input to gain of Mbase and sum pref)
ax.plot(fRange, BAAL_range,ls='-', label =r'BAAL', color =[0, 0, 0])

plt.xlim(59.96, 60.04)
plt.ylim(-1000,1000)
plt.grid(True)
plt.title('Balancing Authority ACE Limit')
plt.xlabel('Frequency [Hz]')
plt.ylabel(r'BAAL [MW]')
plt.legend()

fig.set_dpi(150)
fig.set_size_inches(9*.7, 4.5*.85)
fig.tight_layout()
printFigs = True
if printFigs: plt.savefig('BAAL.pdf', dpi=300)
plt.show(block = True)
plt.pause(0.00001)