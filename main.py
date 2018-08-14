import sys
import atexit
import functools
import time
from datetime import datetime
from datetime import timedelta
from dateutil import parser
import re
import RPi.GPIO as GPIO
import serial
import json
import threading
import mainwindow_auto
import random
import setup_auto
import ctypes

from luhn import *
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from barcode import *
from PyQt5.QtWidgets import *
from player import Player
from game import Game
from player import Player
from senddata import SendData
from datafromserial import dataFromSerial

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(29, GPIO.IN)
GPIO.setup(13, GPIO.OUT)

stopSerial = True
isOkSerial = False

wait_time = 0.3
started_time = 0
started_time_light = 0
total_time = 180
counter = 0
counterToSend = 0
lastSensorRnd = 0
lightBlinkTimer = 3000  
totalHits = 0
hammerHits = 0
buttonOne = 0
buttonTwo = 0
buttonThree = 0
buttonFour = 0
buttonFive = 0
buttonSix = 0
rndSensors = []
selectedHammer = QStandardItem()

actual_player = Player()
actual_game = Game()

modelList = QStandardItemModel()

actual_barcode = ""
serialReturn = ""

test = [0,0,0,0,0]

libc = ctypes.CDLL('libc.so.6')

modelList = QStandardItemModel()

class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):

    port = serial.serial_for_url("/dev/serial0", baudrate=9600, timeout=3.0)
    dtSerial = dataFromSerial()

    def cleanup(self):
        self.port.close()
        GPIO.cleanup()

    def binaryToDecimal(self, binary):
        binary1 = binary
        decimal, i, n = 0, 0, 0
        while(binary != 0):
            dec = binary % 10
            decimal = decimal + dec * pow(2,i)
            binary = binary//10
            i += 1
        return decimal

    def reading(self):
        global serialReturn, totalHits, lastSensorRnd, nextLight
        while 1: 
            raw_reading = self.port.readline()
            try:
                if raw_reading:
                    serialReturn = self.dtSerial.verifyData(raw_reading)
                    if "hit" in serialReturn:
                        tmpReturn = serialReturn.split('-')
                        serialReturn = "hit"
                        if tmpReturn[0] == "hit":
                            print((int(tmpReturn[1])-100))
                            print(lastSensorRnd)
                            if (int(tmpReturn[1])-100) == lastSensorRnd:
                                self.makeHits(int(tmpReturn[1])-100)
                                nextLight = True
                        if tmpReturn[0] == "nohit" and (int(tmpReturn[1])-100) == lastSensorRnd:
                            nextLight = True
            except:
                pass

    def makeHits(self, sensor):
        global hammerHits, buttonOne, buttonTwo, buttonThree, buttonFour, buttonFive, buttonSix

        if sensor == 1:
            buttonOne += 1
        if sensor == 2:
            buttonTwo += 1
        if sensor == 3:
            buttonThree += 1
        if sensor == 4:
            buttonFour += 1
        if sensor == 5:
            buttonFive += 1
        if sensor == 6:
            buttonSix += 1 

        self.lcdOne.display(buttonOne)
        self.lcdTwo.display(buttonTwo)
        self.lcdThree.display(buttonThree)
        self.lcdFour.display(buttonFour)
        self.lcdFive.display(buttonFive)
        self.lcdSix.display(buttonSix)

    def readingHammer(self, channel):
        global test, hammerHits
        # while 1: 
        if GPIO.input(29) == True:
            time.sleep(0.025) 
            test[0] = GPIO.input(29)
            time.sleep(0.01)
            test[1] = GPIO.input(29)
            time.sleep(0.01)
            test[2] = GPIO.input(29)
            time.sleep(0.01)
            test[3] = GPIO.input(29)
            time.sleep(0.01)
            test[4] = GPIO.input(29)
            time.sleep(0.01)
            print(test)
            tmp = ''.join(map(str,test[0:3]))
            hitFrom = self.binaryToDecimal(int(tmp))
            print(hitFrom)
            if hitFrom == lastSensorRnd:
                self.stopLight(lastSensorRnd)
                self.callSensor()
                nextLight = True
                hammerHits += 1
                self.lcdSeven.display(hammerHits)               

            # GPIO.output(13, 1)
            # time.sleep(0.05)
            # GPIO.output(13, 0)
                

    def showAlert(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.setWindowTitle("Alerta")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def pressedAddButton(self):
        global modelList
        print("scan")
        barcode =  barcode_reader()
        print(barcode)
        print(modelList.findItems(barcode))
        
        if len(modelList.findItems(barcode)) > 0:
            self.showAlert('Credencial em uso!!')
            return

        nu = re.findall(r'\d+',barcode)
        print(nu[0])
        if verify(nu[0]) == False:
            self.showAlert('Erro ao ler credencial!')
        else:
            item = QStandardItem(barcode)
            modelList.appendRow(item)
            if modelList.rowCount() >= 1:
                # self.btnTest.setEnabled(True)
                self.btnRemove.setEnabled(True)
                self.btnHammer.setEnabled(True)
            if modelList.rowCount() == 7:
                self.btnAdd.setEnabled(False)


    def pressedRemoveButton(self):
        global modelList
        for index in self.lstViewCodes.selectedIndexes():
            modelList.removeRow(index.row())

        if modelList.rowCount() >= 1:
            self.btnHammer.setEnabled(True)
        if modelList.rowCount() <= 7:
            self.btnAdd.setEnabled(True)
        if modelList.rowCount() == 0:
            self.btnStart.setEnabled(False)
            # self.btnTest.setEnabled(False)
            self.btnRemove.setEnabled(False)
            self.btnHammer.setEnabled(False)
        
    def startSensor(self):
        global isOkSerial, wait_time
        
        for x in range(5):
            print(">{0},{1};".format(x+1, 1))
            isOkSerial = False
            GPIO.output(7, GPIO.HIGH)
            time.sleep(0.05)
            self.port.write(">{0},{1};".format(x+1, 1))
            time.sleep(0.05)
            GPIO.output(7, GPIO.LOW)
            print("before while")
            time.sleep(wait_time)
            print("after while")
            self.statusSensor(x, isOkSerial)
            self.btnStart.setEnabled(True)

    def statusSensor(self, sensor, isok):
        if sensor == 0:
            if isok:
                self.lcdNumber.setStyleSheet("QWidget {color: green}")
            else:
                self.lcdNumber.setStyleSheet("QWidget {color: red}")
        if sensor == 1:
            if isok:
                self.lcdNumber.setStyleSheet("QWidget {color: green}")
            else:
                self.lcdNumber.setStyleSheet("QWidget {color: red}")
        if sensor == 2:
            if isok:
                self.lcdNumber.setStyleSheet("QWidget {color: green}")
            else:
                self.lcdNumber.setStyleSheet("QWidget {color: red}")
        if sensor == 3:
            if isok:
                self.lcdNumber.setStyleSheet("QWidget {color: green}")
            else:
                self.lcdNumber.setStyleSheet("QWidget {color: red}")
        if sensor == 4:
            if isok:
                self.lcdNumber.setStyleSheet("QWidget {color: green}")
            else:
                self.lcdNumber.setStyleSheet("QWidget {color: red}")

    def sensorTurn(self, sensor):
        self.resetLcdColors()
        if sensor == 1:
            self.lcdOne.setStyleSheet("QWidget {color: blue}")
        if sensor == 2:
            self.lcdTwo.setStyleSheet("QWidget {color: blue}")
        if sensor == 3:
            self.lcdThree.setStyleSheet("QWidget {color: blue}")
        if sensor == 4:
            self.lcdFour.setStyleSheet("QWidget {color: blue}")
        if sensor == 5:
            self.lcdFive.setStyleSheet("QWidget {color: blue}")                
        if sensor == 6:
            self.lcdSix.setStyleSheet("QWidget {color: blue}")                
        if sensor == 7:
            self.lcdSeven.setStyleSheet("QWidget {color: blue}")                

    def resetLcdColors(self):
        self.lcdOne.setStyleSheet("QWidget {color: black}")
        self.lcdTwo.setStyleSheet("QWidget {color: black}")
        self.lcdThree.setStyleSheet("QWidget {color: black}")
        self.lcdFour.setStyleSheet("QWidget {color: black}")
        self.lcdFive.setStyleSheet("QWidget {color: black}")   
        self.lcdSix.setStyleSheet("QWidget {color: black}")   
        self.lcdSeven.setStyleSheet("QWidget {color: black}")   

    def secondsToStr(self, t):
        rediv = lambda ll,b : list(divmod(ll[0],b))+ll[1:]
        return "%d:%02d:%02d.%03d" % tuple(reduce(rediv,[[t*1000,],1000,60,60]))

    def pressedConfigButton(self):  
        self.dialog.show()

    def pressedStartButton(self):
        print("start")

        global started_time, actual_player, actual_game, lightBlinkTimer, total_time, totalHits, hammerHits, buttonOne, buttonTwo, buttonThree, buttonFour, buttonFive, buttonSix

        self.btnStart.setEnabled(False)
        
        hammerHits = 0
        buttonOne = 0
        buttonTwo = 0
        buttonThree = 0
        buttonFour = 0
        buttonFive = 0
        buttonSix = 0

        self.lcdOne.display(buttonOne)
        self.lcdTwo.display(buttonTwo)
        self.lcdThree.display(buttonThree)
        self.lcdFour.display(buttonFour)
        self.lcdFive.display(buttonFive)
        self.lcdSix.display(buttonSix)
        self.lcdSeven.display(hammerHits)
        
        started_time = time.time()
        self.timerOne.start(1)
        
        actual_player = Player()
        actual_game = Game()
        actual_game.startTime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        
        self.callSensor()

    def Time(self, lcd):
        global started_time, actual_player, counter, serialReturn, isOkSerial, counterToSend, lightBlinkTimer
        counter += 1
        counterToSend += 1
        elapsed = time.time() - started_time 
        
        timer = self.secondsToStr(elapsed)[:-4]

        lcd.setDigitCount(len(timer))
        lcd.display(timer)

        if serialReturn != "ok" and not isOkSerial:
            if counter >= lightBlinkTimer + 1500:
                # CALL ANOTHER LIGHT
                counter = 0
                if counterToSend >= 100:
                    self.callSensor()
                    counterToSend = 0
        elif serialReturn == "nohit" or serialReturn == "hit":
            counter = 0
            if counterToSend >= 100:
                self.callSensor()
                counterToSend = 0
            # CALL ANOTHER LIGH
        elif serialReturn == "ok":
            counter = 0
            isOkSerial = True
            
        serialReturn = ""

        if int(elapsed) >= total_time:
            print("done")
            self.stopTimer(True)
            counter = 0

    
    def callSensor(self):
        global lastSensorRnd, isOkSerial, rndSensors, started_time_light
        started_time_light = time.time()
        elapsed = 0
        while elapsed >= 1:
            elapsed = time.time() - started_time 

        rndSensor = random.randint(1, 6)
        print("SensorRnd: {0}".format(rndSensor))
        # if rndSensor == lastSensorRnd:
        if rndSensor in rndSensors:
            self.callSensor()
        else:
            rndSensors.append(rndSensor)
            lastSensorRnd = rndSensor
            self.sensorTurn(lastSensorRnd)
            isOkSerial = False
            GPIO.output(7, GPIO.HIGH)
            time.sleep(0.05)
            self.port.write(">{0},{1};".format(rndSensor, lightBlinkTimer))
            time.sleep(0.05)
            GPIO.output(7, GPIO.LOW)

        if len(rndSensors) == 6:
            rndSensors = []

    def stopLight(self, rndSensor):
        GPIO.output(7, GPIO.HIGH)
        time.sleep(0.05)
        self.port.write(">{0},stop;".format(rndSensor))
        time.sleep(0.05)
        GPIO.output(7, GPIO.LOW)

    def pressedTestButton(self):
        self.lcdNumber.setStyleSheet("QWidget {color: black}")
        # self.btnTest.setEnabled(False)
        self.startSensor()

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        
        timerOneCallback = functools.partial(self.Time, lcd=self.lcdNumber)

        self.timerOne = QtCore.QTimer(self)
        self.timerOne.timeout.connect(timerOneCallback)

        self.btnAdd.clicked.connect(lambda: self.pressedAddButton())
        self.btnRemove.clicked.connect(lambda: self.pressedRemoveButton())
        self.btnStart.clicked.connect(lambda: self.pressedStartButton())
        self.btnHammer.clicked.connect(lambda: self.pressedHammerButton())
        self.btnStop.clicked.connect(lambda: self.stopTimer(False))
        # self.btnTest.clicked.connect(lambda: self.pressedTestButton())

        self.lstViewCodes.setModel(modelList)

        reading_thread = threading.Thread(target=self.reading)
        reading_thread.daemon = True
        reading_thread.start()    

        GPIO.add_event_detect(29, GPIO.BOTH, callback=self.readingHammer)

        # readingHammer_thread = threading.Thread(target=self.reading)
        # readingHammer_thread.daemon = True
        # readingHammer_thread.start()

        atexit.register(self.cleanup)

    def pressedHammerButton(self):
        global modelList, selectedHammer

        index = random.randint(0,modelList.rowCount()-1)
        selectedHammer = modelList.takeItem(index)
        modelList.removeRow(index)
        modelList.insertRow(0, selectedHammer)
        self.showAlert("Participante com Martelo: " + selectedHammer.text())
        self.btnHammer.setEnabled(False)
        self.lstViewCodes.setSelectionMode(QAbstractItemView.NoSelection)
        self.btnStart.setEnabled(True)
        

    def stopTimer(self, auto):

        global actual_player, actual_game, actual_barcode, totalHits, hammerHits, buttonOne, buttonTwo, buttonThree, buttonFour, buttonFive, buttonSix, selectedHammer

        self.timerOne.stop()
        self.btnStart.setEnabled(False)
        self.btnStop.setEnabled(False)

        # for x in range(5):
        #     print(x)
        #     GPIO.output(7, GPIO.HIGH)
        #     time.sleep(0.05)
        #     self.port.write(">{0},{1};".format(x+1, 2))
        #     time.sleep(0.05)
        #     GPIO.output(7, GPIO.LOW)
        #     time.sleep(wait_time)


        for index in range(modelList.rowCount()):
            actual_player = Player()
            if index == 0:
                if hammerHits > 0:
                    actual_player.addAction("HIT_HAMMER", hammerHits) 
            if index == 1:
                if buttonOne > 0:
                    actual_player.addAction("PUSH_BUTTON", buttonOne)
            if index == 2:
                if buttonTwo > 0:
                    actual_player.addAction("PUSH_BUTTON", buttonTwo)
            if index == 3:
                if buttonThree > 0:
                    actual_player.addAction("PUSH_BUTTON", buttonThree)
            if index == 4:
                if buttonFour > 0:
                    actual_player.addAction("PUSH_BUTTON", buttonFour)
            if index == 5:
                if buttonFive > 0:
                    actual_player.addAction("PUSH_BUTTON", buttonFive)
            if index == 6:
                if buttonSix > 0:
                    actual_player.addAction("PUSH_BUTTON", buttonSix)                

            actual_player.token = modelList.item(index).text()
            actual_game.players.append(actual_player)

        modelList.clear()
        
        actual_game.finishTime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

        self.lstViewCodes.setSelectionMode(QAbstractItemView.SingleSelection)

        if auto == True:
            #Send Data
            threading.Thread(target=SendData().send_to_calindra, args=(actual_game.toJSON(),"WHACK_A_FRIEND"), kwargs={}).start()
        

def main():
    app = QApplication(sys.argv)
    # app.setOverrideCursor(Qt.BlankCursor)
    form = MainWindow()
    form.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()