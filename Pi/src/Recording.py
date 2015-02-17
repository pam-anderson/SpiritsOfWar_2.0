import alsaaudio
import wave
import numpy

class recordSnd:
    def __init__(self):
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
        inp.setchannels(1)
        inp.setrate(44100)
        inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        inp.setperiodsize(1024)
    def recordSound(self, filename):
        w=wave.open(filename, 'w')
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(44100)
        while True:
            data = inp.read()
            w.writeframes(data)
