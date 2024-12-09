import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import wave
from scipy.fft import rfft, rfftfreq

CHUNK = 1024 * 4 # how much audio is displayd
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100 #kHz
FFT_WINDOW_SIZE = 1

def clamp(min_value, max_value, value):

    if value < min_value:
        return min_value

    if value > max_value:
        return max_value

    return value

p = pyaudio.PyAudio() #pyaudio object
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK,
    input_device_index=2
)

# Get the number of audio I/O devices
devices = p.get_device_count()



def generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    # 2pi because np.sin takes radians
    y = np.sin((2 * np.pi) * frequencies)
    return x, y

_, nice_tone = generate_sine_wave(400, CHUNK, FFT_WINDOW_SIZE)
_, noise_tone = generate_sine_wave(4000, CHUNK, FFT_WINDOW_SIZE)
noise_tone = noise_tone * 0.3

mixed_tone = nice_tone + noise_tone

normalized_tone = np.int16((mixed_tone / mixed_tone.max()) * 4096)

# Number of samples in normalized_tone
N = CHUNK * FFT_WINDOW_SIZE
yf = rfft(normalized_tone)
xf = rfftfreq(N, 1 / CHUNK)


print("start recording")

plt.ion()
fig, ax = plt.subplots()
x = np.arange((CHUNK / 2) + 1) / (float(CHUNK) / RATE)
#x = np.arange(0, 2*CHUNK,2)
line, = ax.plot(xf, np.abs(yf))
line.set_xdata(xf)
line.set_ydata(np.abs(yf))
print(len(np.abs(yf)))
#ax.set_xlim(0, 2*CHUNK)
#ax.set_ylim(0,yf.max())



while True:
    data = stream.read(CHUNK)
    #print(data)
    amplitude = np.fromstring(data, np.int16)
    normalized_amplitude = np.int16((amplitude/amplitude.max())*31767)
    #print(normalized_amplitude)
    normalized_amplitude = normalized_amplitude * np.hamming(len(normalized_amplitude))
    yf = rfft(normalized_amplitude)
    abs_yf = np.abs(yf)
    #print(len(np.abs(yf)))
    #xf = rfftfreq(N, 1 / RATE)
    #line.set_ydata(normalized_amplitude)
    line.set_ydata(abs_yf)
    #plt.plot(xf, np.abs(yf))
    fig.canvas.draw()
    fig.canvas.flush_events()

#print(len(frames))
#frames = struct.unpack(str(2*CHUNK) + 'B', frames[0])
stream.start_stream()
stream.close()
p.terminate()
