import pygame

# -------------- IMPORTANT!! ----------------
# Run the following command first!
# sudo amixer cset numid=3 1
# -------------------------------------------

class Sound:
    def __init__(self):
        self.sfx = []
        self.readyPin = 5
        self.donePin = 3
        # The DE2 only ever sends 1 type of msg: recorded sound
        self.dataPins = [7, 8, 10, 11, 12, 13, 15, 16, 18, 22, 29, 31,
            32, 33, 35, 36, 37, 38, 40]
        # Load main music
        pygame.mixer.init()
        pygame.mixer.music.load("mus.wav") # load main music
        pygame.mixer.music.play(-1) # -1 for infinite loop
        # can append more depending on # of SFX
        self.sfx.append(pygame.mixer.Sound("war.wav")) 
        # Load sound effects
        self.sfx.append(pygame.mixer.Sound("arch.wav"))
        self.sfx.append(pygame.mixer.Sound("mag.wav"))
        self.sfx.append(pygame.mixer.Sound("mov.wav"))
        self.sfx.append(pygame.mixer.Sound("die.wav"))

    def play_sfx(self, sfx_num):
        self.sfx[sfx_num].play(0) #0 for repeat once 

    # Must be called each time Pi is changed to reader
    def setGpios(self):
        GPIO.setmode(GPIO.BOARD)
        for pin in self.dataPins:
            GPIO.setup(pin, GPIO.OUT)
        GPIO.setup(self.readyPin, GPIO.IN)
        GPIO.setup(self.donePin, GPIO.OUT)

    def getData(self):
        # Wait for ready flag to be set
        while not GPIO.input(self.readyPin):
            pass
        out = 0
        for pin in range(16):
            out = (out << 1) | self.dataPins[pin]
        # Set done flag
        GPIO.output(self.donePin, 1)
        # Wait for ready flag to be cleared
        while GPIO.input(self.readyPin):
            pass
        # Clear done flag
        GPIO.output(self.donePin, 0)
        return out

    def isRecordingDone(self, data):
        if data is 0xFFFF:
            return True
        else:
            return False

    def getSound(self):
        # Read sound info from GPIOs
        sound = self.getData()
        while not self.isRecordingDone(sound):
            # SAVE SOUND TO FILE
            sound = self.getData()
        GPIO.cleanup()
