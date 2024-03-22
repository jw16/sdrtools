import numpy as np
import matplotlib.pyplot as plt
import sys


def toreal(sig, fc=1e6, fs = 1e6) :
    t_u = np.arange(len(sig))/fs
    nsig =  np.real(sig) * np.cos(2*np.pi*t_u*fc) - np.imag(sig)* np.sin(2*np.pi*t_u*fc)
    return nsig


Fs = 1e6
Fc = 91.5e6
bsize = 16384


usesdr=sys.argv[1]
if len(sys.argv) > 3 :
    Fs = float(sys.argv[2])
    Fc = float(sys.argv[3])
    

# set this to True if you have the HackRF plugged in


if usesdr == "HackRF" :
    from  hackrf import *
    hackrf = HackRF()

    # the sample rate of the receiver - how many
    # samples per second to record energy from the antenna
    hackrf.sample_rate = Fs
    # The carrier frequency / center frequency
    hackrf.center_freq = Fc

    # we read 'bsize` samples, which would be bsize / Fs seconds of data
    buff = hackrf.read_samples(bsize)
    print(len(buff), buff.dtype)

# set this to True if you have an RTLSDR plugged in

if usesdr == "RTLSDR" :
    import rtlsdr
    sdr = rtlsdr.RtlSdr()
    sdr.center_freq = Fc
    sdr.sample_rate = Fs
    buff = sdr.read_samples(bsize)
    print(len(buff), buff.dtype)


# SDR's return IQ samples - stored as complex numbers
# we use Fc and Fs to convert back to the raw time-series
# signal that was seen "over the air" 
X = toreal(buff, fs=Fs, fc=Fc)

# create the plot window
fig = plt.figure()
# create 2 sub-plots
ax, ax2 = fig.subplots(2)
    
# take an FFT of all 16K samples
Y    = np.fft.fftshift(np.fft.fft(buff))
# this converts the complex FFT outputs to dB
ydb = 20 * np.log10(np.abs(Y)+1e-9)

# fftshift swaps the 2 halves of the FFT output so the
# frequency bin corresponding to 0 (Fc) is in the middle
freq = np.fft.fftshift(np.fft.fftfreq(bsize, 1e-6))
freq += Fc


# fftfreq returns relative frequencies, so we add in our center 
# convert to MHz for convenience
freq *= 1e-6
line1, = ax.plot(freq, ydb, 'b-')
ax.set_ylim(-20, 50)
line2, = ax2.plot(X[0:128])
ax2.set_ylim(-1, 1)

plt.show()


# recreate the figure so it can be refreshed with new data
# You probably won't need this if you're embedding things in a tkinter plot...
plt.ion()
fig = plt.figure()
ax, ax2 = fig.subplots(2)
line1, = ax.plot(freq, ydb, 'b-')
ax.set_ylim(-20, 50)
line2, = ax2.plot(X[0:128])
ax2.set_ylim(-1, 1)

#sys.exit(1)

for i in range(1000000000) :
    # read more samples
        
    if usesdr=="RTLSDR" :
        buff = sdr.read_samples(bsize)
    else:
        buff = hackrf.read_samples(bsize)

    # compute FFT
    Y    = np.fft.fftshift(np.fft.fft(buff))
    # convert to DB
    ydb = 20 * np.log10(np.abs(Y)+1e-9)
    # plot spectrum
    line1.set_ydata(ydb)
    
    X = toreal(buff, fs=Fs, fc=Fc)

    # plot time-domain signal 
    line2.set_ydata(X[0:128])
    fig.canvas.draw()
    fig.canvas.flush_events()


    

print("exit?")
x = sys.stdin.readline()
