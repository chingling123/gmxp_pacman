import sys
import atexit
import functools
import time
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
from RF24 import *
from datetime import datetime
from datetime import timedelta
from dateutil import parser
from config import Config
from zabbix_gmxp import SendDataZabbix

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

radio = RF24(22, 0);

pipes = [0x65646f4e32, 0x65646f4e31]
min_payload_size = 4
max_payload_size = 32
payload_size_increments_by = 1
next_payload_size = min_payload_size
inp_role = 'none'
send_payload = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ789012'
millis = lambda: int(round(time.time() * 1000))
radio.begin()
radio.enableAckPayload()
radio.setRetries(0,15)
radio.setAutoAck(1)
radio.setChannel(20)
radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1,pipes[0])
radio.printDetails()
radio.startListening()

stopSerial = True
isOkSerial = False

wait_time = 0.3
started_time = 0
started_time_light = 0
started_time_pacman = 0
isPacman = False
total_time = 180
counter = 0
counterToSend = 0
lastSensorRnd = 0
lightBlinkTimer = 3000  
totalHits = 0
pacVitamin = 0
buttonOne = 0
buttonTwo = 0
buttonThree = 0
buttonFour = 0
buttonFive = 0
killPhatom = 0
vitaminTime = 20
pacLifes = 1

selectedPacman = QStandardItem()

actual_player = Player()
actual_game = Game()

modelList = QStandardItemModel()

actual_barcode = ""
serialReturn = ""

test = [0,0,0,0,0]

settings = []

libc = ctypes.CDLL('libc.so.6')

modelList = QStandardItemModel()

class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):

    port = serial.serial_for_url("/dev/serial0", baudrate=9600, timeout=3.0)
    dtSerial = dataFromSerial()

    def cleanup(self):
        self.onLightOut("000")
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
        global serialReturn, pacVitamin
        while 1: 
            raw_reading = self.port.readline()
            try:
                if raw_reading:
                    print(raw_reading)
                    serialReturn = self.dtSerial.verifyData(raw_reading)
                    if "hit" in serialReturn:
                        tmpReturn = serialReturn.split('-')
                        serialReturn = "hit"
                        if tmpReturn[0] == "hit":
                            print(tmpReturn[1])
                            if int(tmpReturn[1]) <= 104:
                                self.sendPacManVitamin()
                            elif int(tmpReturn[1]) == 130:
                                self.sendRevivPacman()
                            else:
                                self.makeHits(5)
                                
            except:
                pass

    def makeHits(self, sensor):
        global pacVitamin, buttonOne, buttonTwo, buttonThree, buttonFour, pacLifes, killPhatom

        if sensor == 1 and not isPacman:
            buttonOne += 1
            pacLifes -= 1
            self.onLight(30, settings['pacman'])
        if sensor == 2 and not isPacman:
            buttonTwo += 1
            pacLifes -= 1
            self.onLight(30, settings['pacman'])
        if sensor == 3 and not isPacman:
            buttonThree += 1
            pacLifes -= 1
            self.onLight(30, settings['pacman'])
        if sensor == 4 and not isPacman:
            buttonFour += 1
            pacLifes -= 1
            self.onLight(30, settings['pacman'])
        if sensor == 5:
            pacVitamin += 1
        if sensor == 6:
            killPhatom += 1

        self.lcdOne.display(buttonOne)
        self.lcdTwo.display(buttonTwo)
        self.lcdThree.display(buttonThree)
        self.lcdFour.display(buttonFour)
        self.lcdPac.display(pacVitamin)
        self.lifeBar.setValue(pacLifes)
        if pacVitamin >= 25:
            self.stopTimer(True)
        

    def sendNoPacmVitamin(self):
        print("send no vitamin")
        self.onLightOut("001")
        time.sleep(0.1)
        radio.stopListening()
        # Send the final one back.
    
        radio.write("nopac>{0};".format(settings['pacman']))
        # Now, resume listening so we catch the next packets.
        radio.startListening()
        

    def sendRevivPacman(self):
        time.sleep(0.1)
        print("send revive")
        radio.stopListening()
        # Send the final one back.    
        radio.write("reviv>{0};".format(settings['pacman']))
        # Now, resume listening so we catch the next packets.
        radio.startListening()   

    def sendPacManVitamin(self):
        global isPacman, started_time_pacman
        print("send vitamin")
        self.onLightOut("100")
        time.sleep(0.1)
        radio.stopListening()
        # Send the final one back.
        radio.write("pacma>{0};".format(settings['pacman']))
        # Now, resume listening so we catch the next packets.
        radio.startListening()
        
        started_time_pacman = time.time()
        isPacman = True
                
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
                self.btnRemove.setEnabled(True)
                self.btnHammer.setEnabled(True)
            if modelList.rowCount() == 5:
                self.btnAdd.setEnabled(False)

    def pressedRemoveButton(self):
        global modelList
        for index in self.lstViewCodes.selectedIndexes():
            modelList.removeRow(index.row())

        if modelList.rowCount() >= 1:
            self.btnHammer.setEnabled(True)
        if modelList.rowCount() <= 5:
            self.btnAdd.setEnabled(True)
        if modelList.rowCount() == 0:
            self.btnStart.setEnabled(False)
            self.btnRemove.setEnabled(False)
            self.btnHammer.setEnabled(False)
        
    def startLights(self):
        global isOkSerial, wait_time
        
        for x in range(29):
            print(">{0},{1};".format(x+1, settings['pacman']))
            self.onLight(x+1, settings['pacman'])
            time.sleep(wait_time)

        print("done")
        self.onLightOut("001")    

    def resetLcdColors(self):
        self.lcdOne.setStyleSheet("QWidget {color: black}")
        self.lcdTwo.setStyleSheet("QWidget {color: black}")
        self.lcdThree.setStyleSheet("QWidget {color: black}")
        self.lcdFour.setStyleSheet("QWidget {color: black}")
        self.lcdFive.setStyleSheet("QWidget {color: black}")   

    def secondsToStr(self, t):
        rediv = lambda ll,b : list(divmod(ll[0],b))+ll[1:]
        return "%d:%02d:%02d.%03d" % tuple(reduce(rediv,[[t*1000,],1000,60,60]))

    def pressedStartButton(self):
        print("start")

        global started_time, actual_player, actual_game, lightBlinkTimer, total_time, pacVitamin, buttonOne, buttonTwo, buttonThree, buttonFour, pacLifes
        
        self.btnStart.setEnabled(False)
        
        pacVitamin = 0
        buttonOne = 0
        buttonTwo = 0
        buttonThree = 0
        buttonFour = 0
        killPhatom = 0
        pacLifes = 1

        self.lcdOne.display(buttonOne)
        self.lcdTwo.display(buttonTwo)
        self.lcdThree.display(buttonThree)
        self.lcdFour.display(buttonFour)
        self.lcdPac.display(pacVitamin)
        self.lifeBar.setValue(pacLifes)

        self.startLights()
        self.onLightOut("001")
        self.startGame()
        
        started_time = time.time()
        self.timerOne.start(1)
        
        actual_player = Player()
        actual_game = Game()
        actual_game.startTime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        
        threading.Thread(target=SendDataZabbix().send_zabbix, args=("gxp-pm01", "start", 2), kwargs={}).start()

    def startGame(self):
        radio.stopListening()
        # Send the final one back.
        radio.write("start>{0};".format(settings['pacman']))
        # Now, resume listening so we catch the next packets.
        radio.startListening()        

    def TimeVitamin(self):
        global started_time_pacman
        elapsed = time.time() - started_time_pacman
        if int(elapsed) >= vitaminTime:
            print('no ispacman')
            self.timerTwo.stop()
            self.sendNoPacmVitamin()
    
    def Time(self, lcd):
        global started_time, actual_player, counter, serialReturn, isOkSerial, counterToSend, lightBlinkTimer, isPacman, pacVitamin, buttonOne, buttonTwo, buttonThree, buttonFour, pacLifes

        if pacLifes < 0:
            self.stopTimer(True)

        if isPacman == True:
            isPacman = False
            self.timerTwo.start(1)

        if radio.available():
            while radio.available():
                print('available')
                lent = radio.getDynamicPayloadSize()
                receive_payload = radio.read(lent)
                print('Got payload size={} value="{}"'.format(lent, receive_payload))
                if int(receive_payload[:-4]) == int(settings["blue"]):
                    self.makeHits(1)
                if int(receive_payload[:-4]) == int(settings["red"]):
                    self.makeHits(2)                   
                if int(receive_payload[:-4]) == int(settings["orange"]):
                    self.makeHits(3)
                if int(receive_payload[:-4]) == int(settings["purple"]):
                    self.makeHits(4)
                if int(receive_payload[:-4]) == int(settings["pacman"]):
                    self.makeHits(6)  
                if int(receive_payload[:4]) == 130:
                    self.sendRevivPacman()

        counter += 1
        counterToSend += 1
        elapsed = time.time() - started_time 
        
        timer = self.secondsToStr(elapsed)[:-4]

        lcd.setDigitCount(len(timer))
        lcd.display(timer)

        if int(elapsed) >= total_time:
            print("done")
            self.stopTimer(True)

    def onLightOut(self, color):
        GPIO.output(7, GPIO.HIGH)
        time.sleep(0.05)
        self.port.write(">62,{0};".format(color))
        time.sleep(0.05)
        GPIO.output(7, GPIO.LOW)

    def onLight(self, sensor, pacman):
        GPIO.output(7, GPIO.HIGH)
        time.sleep(0.05)
        self.port.write(">{0},{1};".format(sensor, pacman))
        time.sleep(0.05)
        GPIO.output(7, GPIO.LOW)


    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        global settings
        
        timerOneCallback = functools.partial(self.Time, lcd=self.lcdNumber)

        self.timerOne = QtCore.QTimer(self)
        self.timerOne.timeout.connect(timerOneCallback)

        self.timerTwo = QtCore.QTimer(self)
        self.timerTwo.timeout.connect(lambda: self.TimeVitamin())

        self.btnAdd.clicked.connect(lambda: self.pressedAddButton())
        self.btnRemove.clicked.connect(lambda: self.pressedRemoveButton())
        self.btnStart.clicked.connect(lambda: self.pressedStartButton())
        self.btnHammer.clicked.connect(lambda: self.pressedHammerButton())
        self.btnStop.clicked.connect(lambda: self.stopTimer(True))

        self.lstViewCodes.setModel(modelList)
        self.lifeBar.setMaximum(pacLifes)

        reading_thread = threading.Thread(target=self.reading)
        reading_thread.daemon = True
        reading_thread.start()    

        settings = Config().read_or_new_pickle('settings.dat', dict(pacman="0", blue="0", red="0", orange="0", purple="0"))
        print(settings)

        time.sleep(0.1)
        self.onLightOut("000")
        atexit.register(self.cleanup)

    def pressedHammerButton(self):
        global modelList, selectedPacman
        index = random.randint(0,modelList.rowCount()-1)
        selectedPacman = modelList.takeItem(index)
        modelList.removeRow(index)
        modelList.insertRow(0, selectedPacman)
        self.btnHammer.setEnabled(False)
        self.lstViewCodes.setSelectionMode(QAbstractItemView.NoSelection)
        self.btnStart.setEnabled(True)
        

    def stopTimer(self, auto):
        global killPhatom, actual_player, actual_game, actual_barcode, totalHits, pacVitamin, buttonOne, buttonTwo, buttonThree, buttonFour, selectedPacman
        self.timerTwo.stop()
        self.timerOne.stop()
        self.onLightOut("000")
        self.btnStart.setEnabled(False)
        self.btnAdd.setEnabled(True)
        self.btnRemove.setEnabled(False)

        for index in range(modelList.rowCount()):
            actual_player = Player()

            if index == 0:
                if pacVitamin > 0:
                    actual_player.addAction("EAT_VITAMIN", pacVitamin) 
                if killPhatom > 0:
                    actual_player.addAction("KILL_PHANTOM", killPhatom)                     
            if index == 1:
                if buttonOne > 0:
                    actual_player.addAction("KILL_PAC_MAN", buttonOne)
            if index == 2:
                if buttonTwo > 0:
                    actual_player.addAction("KILL_PAC_MAN", buttonTwo)
            if index == 3:
                if buttonThree > 0:
                    actual_player.addAction("KILL_PAC_MAN", buttonThree)
            if index == 4:
                if buttonFour > 0:
                    actual_player.addAction("KILL_PAC_MAN", buttonFour)            

            actual_player.token = modelList.item(index).text()
            actual_game.players.append(actual_player)

        modelList.clear()
        
        actual_game.finishTime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

        self.lstViewCodes.setSelectionMode(QAbstractItemView.SingleSelection)

        if auto == True:
            #Send Data
            threading.Thread(target=SendData().send_to_calindra, args=(actual_game.toJSON(),"PAC_MAN"), kwargs={}).start()
            threading.Thread(target=SendDataZabbix().send_zabbix, args=("gxp-pm01", "start", 1), kwargs={}).start()
        

def main():
    app = QApplication(sys.argv)
    app.setOverrideCursor(Qt.BlankCursor)
    form = MainWindow()
    form.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()