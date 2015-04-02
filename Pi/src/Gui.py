from Tkinter import *

class guiVideoRec():
    def team_one_warrior(self):
        recordVideo('p0c0.avi')
    def team_one_archer(self):
        recordVideo('p0c1.avi')
    def team_one_mage(self):
        recordVideo('p0c.avi')    
    def team_two_warrior(self):
        recordVideo('p1c0.avi')
    def team_two_archer(self):
        recordVideo('p1c1.avi')
    def team_two_mage(self): 
        recordVideo('p1c2.avi')
    def done_recording(self):
        self.quitButton.grid()
    def createButton(self):
        master = Tk()
	master.title('Video Recording')
        t1_header = Text(master, height = 2, width = 15)
        t1_war = Button(master, text="Warrior", command=self.team_one_warrior)
        t1_arch = Button(master, text="Archer", command=self.team_one_archer)
        t1_mage = Button(master, text="Mage", command=self.team_one_mage)
        t2_header = Text(master, height = 2, width = 15)
        t2_war = Button(master, text="Warrior", command=self.team_two_warrior)
        t2_arch = Button(master, text="Archer", command=self.team_two_archer)
        t2_mage = Button(master, text="Mage", command=self.team_two_mage)
        t1_header.insert(END, "    Team One")
        t2_header.insert(END, "    Team Two")
        t1_header.pack(); t1_war.pack(); t1_arch.pack(); t1_mage.pack(); 
        t2_header.pack(); t2_war.pack(); t2_arch.pack(); t2_mage.pack();  
        mainloop()


#app = guiVideoRec()
#app.createButton()

class guiSoundRec():
    def recWar(self):
        recordSound('rec_war.wav')
    def recArch(self):
        recordSound('rec_arch.wav')
    def recMag(self):
        recordSound('rec_mag.wav')
    def recMov(self):
        recordSound('rec_mov.wav')
    def recDie(self):
        recordSound('rec_die.wav')
    def createButton(self):
        master = Tk()
        master.title('Sound Recording')
        rec_warrior = Button(master, text="Warrior Attack", command=self.recWar)
        rec_archer = Button(master, text="Archer Attack", command=self.recArch)
        rec_mage = Button(master, text="Mage Attack", command=self.recMag)
        rec_move = Button(master, text="Movement", command=self.recMov)
        rec_die = Button(master, text="Death", command= self.recDie)
        rec_warrior.pack(); rec_archer.pack(); rec_mage.pack(); rec_move.pack(); rec_die.pack()
        mainloop()

#app2 = guiSoundRec()
#app2.createButton()
