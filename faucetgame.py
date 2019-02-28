from tkinter import Tk, Entry, Label, Button, StringVar
from pyautogui import click
from threading import Thread
from time import sleep


class Create_GUI:
    
    def __init__(self):
        self.create_MainGUI()
        self.create_pos_input()
        self.create_playbtn()
        self.create_status()
        self.control = [0]
    
    def create_MainGUI(self):
        self.root = Tk()
        self.root.geometry("220x120")
        self.root.resizable(False,False)
        self.root.protocol("WM_DELETE_WINDOW", self.exit_GUI)

    def create_pos_input(self):
        Label(self.root, text="x").place(x=20, y=10, height=20, width=10)
        self.x = Entry(self.root, justify="center")
        self.x.place(x=40, y=10, height=20, width=50)
        Label(self.root, text="y").place(x=130, y=10, height=20, width=10)
        self.y = Entry(self.root, justify="center")
        self.y.place(x=150, y=10, height=20, width=50)

    def create_playbtn(self):
        self.btn = StringVar()
        self.btn.set("Start")
        Button(self.root, textvariable=self.btn, command=self.press).place(x=70, y=50, height=30, width=80)

    def press(self):
        if (self.btn.get() == "Start"):
            self.control[0] = 0
            self.btn.set("Pause")
            self.status.set("Running")
            self.thread = play_click(self.control, self.status, self.btn,self.x, self.y)
            self.thread.start()
        else:
            self.control[0] = 1
            self.btn.set("Start")
            self.status.set("Paussing")

    def create_status(self):
        self.status = StringVar()
        self.status.set("Paussing")
        Label(self.root, relief="ridge", textvariable=self.status).place(x=0, y=100, height=20, relwidth=1.0)
        
    def main_loop(self):
        self.root.mainloop()

    def exit_GUI(self):
        self.control[0] = 1
        try:
            self.thread.join()
        except:
            print "thread has finished"
        self.root.destroy()


class play_click(Thread):
    
    def __init__(self, control, status, btn, x, y):
        Thread.__init__(self)
        self.control = control
        self.status = status
        self.btn = btn
        self.x = x
        self.y = y

    def run(self):
        click(x=400, y=10)
        while self.control[0] == 0:
            try:
                x = int(self.x.get())
                y = int(self.y.get())
                click(x=x, y=y)
            except:
                self.status.set("Error input")
                self.btn.set("Start")
                self.control[0] = 1
            sleep(3)


def main():
    root = Create_GUI()
    root.main_loop()

if __name__ == '__main__':
    main()
