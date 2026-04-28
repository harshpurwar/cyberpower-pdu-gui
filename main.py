from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import uic
import sys,time
from PyQt6.QtCore import QTimer
from subprocess import Popen, PIPE

offline=False

lock=False

command = './cyberpower-pdu'
ip = "192.168.0.3"

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.main = uic.loadUi('./main.ui', self)
        # self.main.setWindowState(self.main.windowState() | Qt.WindowState.WindowMaximized)
        if offline:
            self.main.setWindowTitle(self.main.windowTitle()+' (Offline)')
        
        self.main.on1.clicked.connect(lambda x: self.action(id=1, act='on'))
        self.main.on2.clicked.connect(lambda x: self.action(id=2, act='on'))
        self.main.on3.clicked.connect(lambda x: self.action(id=3, act='on'))
        self.main.on4.clicked.connect(lambda x: self.action(id=4, act='on'))
        self.main.on5.clicked.connect(lambda x: self.action(id=5, act='on'))
        self.main.on6.clicked.connect(lambda x: self.action(id=6, act='on'))
        self.main.on7.clicked.connect(lambda x: self.action(id=7, act='on'))
        self.main.on8.clicked.connect(lambda x: self.action(id=8, act='on'))

        self.main.off1.clicked.connect(lambda x: self.action(id=1, act='off'))
        self.main.off2.clicked.connect(lambda x: self.action(id=2, act='off'))
        self.main.off3.clicked.connect(lambda x: self.action(id=3, act='off'))
        self.main.off4.clicked.connect(lambda x: self.action(id=4, act='off'))
        self.main.off5.clicked.connect(lambda x: self.action(id=5, act='off'))
        self.main.off6.clicked.connect(lambda x: self.action(id=6, act='off'))
        self.main.off7.clicked.connect(lambda x: self.action(id=7, act='off'))
        self.main.off8.clicked.connect(lambda x: self.action(id=8, act='off'))

        self.main.cycle1.clicked.connect(lambda x: self.action(id=1, act='reboot'))
        self.main.cycle2.clicked.connect(lambda x: self.action(id=2, act='reboot'))
        self.main.cycle3.clicked.connect(lambda x: self.action(id=3, act='reboot'))
        self.main.cycle4.clicked.connect(lambda x: self.action(id=4, act='reboot'))
        self.main.cycle5.clicked.connect(lambda x: self.action(id=5, act='reboot'))
        self.main.cycle6.clicked.connect(lambda x: self.action(id=6, act='reboot'))
        self.main.cycle7.clicked.connect(lambda x: self.action(id=7, act='reboot'))
        self.main.cycle8.clicked.connect(lambda x: self.action(id=8, act='reboot'))

        self.main.refreshB.clicked.connect(self.update)

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update)
        # if not offline:
            # self.timer.start(5000) # auto update time in ms
        self.update()

    def myQuery(self,id):
        global lock
        if not offline:
            while lock:
                time.sleep(1e-6)
            lock=True        
            with Popen([command, ip, str(id)], stdout=PIPE, text=True) as proc:
                r = proc.stdout.read().strip()
            lock=False
        else:
            r='0'
        return r

    def myWrite(self, id, act):
        global lock
        if not offline:
            while lock:
                time.sleep(1e-6)
            lock=True
            with Popen([command, ip, str(id), act], stdout=PIPE, text=True) as proc:
                r = proc.stdout.read().strip()
            lock=False
        else:
            r='OFF'
        return r

    def action(self,id,act):
        r = self.myWrite(id,act)
        if r=='ON':
            eval("self.main.on"+str(id)+".setStyleSheet('background-color: green;font-weight: 500;')")
            eval("self.main.off"+str(id)+".setStyleSheet('')")
        elif r=='OFF':
            eval("self.main.off"+str(id)+".setStyleSheet('background-color: red;font-weight: 500;')")
            eval("self.main.on"+str(id)+".setStyleSheet('')")
        
    def update(self):
        for ch in range(1,9):
            r = self.myQuery(ch)
            if r == 'ON':
                eval("self.main.on"+str(ch)+".setStyleSheet('background-color: green;font-weight: 500;')")
                eval("self.main.off"+str(ch)+".setStyleSheet('')")
            elif r == 'OFF':
                eval("self.main.off"+str(ch)+".setStyleSheet('background-color: red;font-weight: 500;')")
                eval("self.main.on"+str(ch)+".setStyleSheet('')")
    
    def close(self):
        if not self.inst == None:
            self.inst.close()
        super().close()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
