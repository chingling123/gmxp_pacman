import setup_auto
import sys
import RPi.GPIO as GPIO
import serial
import atexit
import threading
import time

from config import Config
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from datafromserial import dataFromSerial

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

rfidSet = 0

class SetupDialog(QDialog, setup_auto.Ui_Dialog):
    
    port = serial.serial_for_url("/dev/serial0", baudrate=9600, timeout=3.0)
    dtSerial = dataFromSerial()
    
    def cleanup(self):
        self.port.close()
        GPIO.cleanup()
    
    def reading(self):
        while 1: 
            raw_reading = self.port.readline()
            try:
                if raw_reading:
                    serialReturn = self.dtSerial.verifyData(raw_reading)
                    if "hit" in serialReturn:
                        tmpReturn = serialReturn.split('-')
                        if tmpReturn[0] == "hit":
                            print(tmpReturn[1])
                            if rfidSet == 1:
                                self.lblPac.setText(tmpReturn[1])
                            if rfidSet == 2:
                                self.lblBlue.setText(tmpReturn[1])
                            if rfidSet == 3:
                                self.lblRed.setText(tmpReturn[1])                                
                            if rfidSet == 4:
                                self.lblOrange.setText(tmpReturn[1])
                            if rfidSet == 5:
                                self.lblPurple.setText(tmpReturn[1])
            except:
                pass

    def __init__(self, parent=None):
        super(SetupDialog, self).__init__(parent)
        self.setupUi(self)

    def pressedButton(self, button):
        global rfidSet
        rfidSet = button
        print("button")
        GPIO.output(7, GPIO.HIGH)
        time.sleep(0.05)
        self.port.write(">63,1;")
        time.sleep(0.05)
        GPIO.output(7, GPIO.LOW)
        
    def showEvent(self, event):
        super(SetupDialog, self).showEvent(event)
        
        self.settings = Config().read_or_new_pickle('settings.dat', dict(pacman="0", blue="0", red="0", orange="0", purple="0"))
        
        self.lblPac.setText(self.settings["pacman"])
        self.lblBlue.setText(self.settings["blue"])
        self.lblRed.setText(self.settings["red"])
        self.lblOrange.setText(self.settings["orange"])
        self.lblPurple.setText(self.settings["purple"])

        self.btnPac.clicked.connect(lambda: self.pressedButton(1))
        self.btnBlue.clicked.connect(lambda: self.pressedButton(2))
        self.btnRed.clicked.connect(lambda: self.pressedButton(3))
        self.btnOrange.clicked.connect(lambda: self.pressedButton(4))
        self.btnPurple.clicked.connect(lambda: self.pressedButton(5))

        reading_thread = threading.Thread(target=self.reading)
        reading_thread.daemon = True
        reading_thread.start()    

        atexit.register(self.cleanup)

    def accept(self):
        Config().save_pickle('settings.dat', dict(pacman=self.lblPac.text(), blue=self.lblBlue.text(), red=self.lblRed.text(), orange=self.lblOrange.text(), purple=self.lblPurple.text()))
                
        self.close()

def main():
    app = QApplication(sys.argv)
    # app.setOverrideCursor(Qt.BlankCursor)
    form = SetupDialog()
    form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()