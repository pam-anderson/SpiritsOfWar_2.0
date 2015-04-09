import alsaaudio
import wave
import numpy

class recordSnd:
    def __init__(self):
        self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
        self.inp.setchannels(1)
        self.inp.setrate(44100)
        self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.inp.setperiodsize(1024)
    def recordSound(self, filename):
        w=wave.open(filename, 'w')
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(44100)
        total = 0
        while total < 500:
            total += 1
            l, data = self.inp.read()
            w.writeframes(data)
        print "done recording!!!"
