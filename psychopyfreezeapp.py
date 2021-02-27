from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLabel, QPushButton, QWidget, QMessageBox, QLineEdit
from PyQt5.QtCore import QSize

from psychopyfreezelib import PsychopyFreezeLib

import os

import threading

class PsychopyFreezeApp(QMainWindow):
    def __init__(self):

        QMainWindow.__init__(self)
        self.setWindowTitle("Psychopy Freeze")
        self.setFixedSize(QSize(400, 300))

        y = 20
        self.maindirLabel = QLabel(self); self.maindirLabel.move(20, y)
        self.maindirLabel.setText('Path:')

        self.maindirLine = QLineEdit(self); self.maindirLine.move(80, y)
        self.maindirLine.resize(260, 32)

        self.maindirButton = QPushButton(self); self.maindirButton.move(350, y)
        self.maindirButton.setText("...")
        self.maindirButton.clicked.connect(self.load_main_dir)
        self.maindirButton.resize(30, 32)
        
        y += 40
        self.mainfileLabel = QLabel(self); self.mainfileLabel.move(20, y)
        self.mainfileLabel.setText('Main:')
        self.mainfileLine = QLineEdit(self); self.mainfileLine.move(80, y)
        self.mainfileLine.resize(260, 32)

        self.mainfileButton = QPushButton(self); self.mainfileButton.move(350, y)
        self.mainfileButton.setText("...")
        self.mainfileButton.clicked.connect(self.load_main_file)
        self.mainfileButton.resize(30, 32)

        y += 40
        self.splashLabel = QLabel(self); self.splashLabel.move(20, y)
        self.splashLabel.setText('Splash:')
        self.splashLine = QLineEdit(self); self.splashLine.move(80, y)
        self.splashLine.resize(260, 32)
        self.splashLine.setText("SPLASH.bmp")

        self.splashButton = QPushButton(self); self.splashButton.move(350, y)
        self.splashButton.setText("...")
        self.splashButton.clicked.connect(self.load_splash_file)
        self.splashButton.resize(30, 32)

        y += 40
        self.NameLabel = QLabel(self); self.NameLabel.move(20, y)
        self.NameLabel.setText('Name:')
        self.NameLine = QLineEdit(self); self.NameLine.move(80, y)
        self.NameLine.resize(300, 32)

        y += 40
        self.StatusLabel = QLabel(self); self.StatusLabel.move(20, y)
        self.StatusLabel.setText('Status:')
        self.StatusMsg = QLabel(self); self.StatusMsg.move(80, y)
        self.StatusMsg.setText('Standby.')
        self.StatusMsg.resize(300, 32)
        
        y += 40
        self.generateButton = QPushButton("Generate!", self)
        self.generateButton.clicked.connect(self.on_click_generate)
        self.generateButton.resize(300,32)
        self.generateButton.move(80, y)

        self.buttons = (
            self.maindirButton,
            self.mainfileButton,
            self.splashButton,
            self.generateButton
        )
       
    def raise_msg(self,msg):
        
        e = QMessageBox()
        e.setWindowTitle("Psychopy Freeze")
        e.setIcon(QMessageBox.Critical)
        e.setText(msg)
        e.setStandardButtons(QMessageBox.Ok)
        e.exec_()

    def load_main_dir(self):
        
        self.main_path = QFileDialog.getExistingDirectory(self)
        if self.main_path == "": return
        
        self.maindirLine.setText(self.main_path)
        self.NameLine.setText(os.path.basename(self.main_path))
        
        path_contents = os.listdir(self.main_path)

        self.mainfileLine.setText("")
        if "main.py" in path_contents:
            self.mainfileLine.setText(os.path.join(self.main_path, "main.py"))
        else:
            self.raise_msg("No main.py detected in your experiment\n"
                            "Please specify the file that runs your experiment!")

        if "assets" not in path_contents:
            self.raise_msg( "No assets folder deteccted in your experiment.\n"
                            "If you use assets in your experiment,\n"
                            "put them in folder called \"assets\".\n")
            return

    def load_main_file(self):

        self.main_file_path = QFileDialog.getOpenFileName(self)[0]

        if self.main_file_path == "": return

        if not self.main_file_path.endswith(".py"):
            self.raise_msg("Invalid File Type Encountered!")
            return

        self.mainfileLine.setText(self.main_file_path)

    def load_splash_file(self):

        self.splash_path = QFileDialog.getOpenFileName(self)[0]

        if self.splash_path == "": return

        if not self.splash_path.lower().endswith(".bmp"):
            self.raise_msg("Invalid File Type Encountered!")
            return

        self.splashLine.setText(self.splash_path)
    
    def on_click_generate(self):

        if "" in (  self.NameLine.text(), 
                    self.maindirLine.text(),
                    self.mainfileLine.text()):
            self.raise_msg("Please fill in all the fields first!")
            return

        self.export_dir = QFileDialog.getExistingDirectory(
            self, "Where to put finished executable?")
        if self.export_dir == "": return
        self.export_path = os.path.join( self.export_dir,
                self.NameLine.text() 
                if self.NameLine.text().endswith(".exe") 
                else (self.NameLine.text() + ".exe"))

        self.gen_lib = PsychopyFreezeLib(
            self.NameLine.text(),
            self.maindirLine.text(),
            self.mainfileLine.text(),
            self.export_path,
            self.splashLine.text()
        )

        threading.Thread(daemon=True, target=self.build).start()

    def build(self):

        for b in self.buttons: b.setEnabled(False)

        self.StatusMsg.setText('Step (1/5) Running Pyinstaller...')
        self.gen_lib.pyinstaller_build()

        self.StatusMsg.setText('Step (2/5) Injecting More Resources...')
        self.gen_lib.module_inject()

        self.StatusMsg.setText('Step (3/5) Pruning Resources...')
        self.gen_lib.prune_build()

        self.StatusMsg.setText('Step (4/5) Compressing into one executable...')
        self.gen_lib.NSIS_build()

        self.StatusMsg.setText('Step (5/5) Cleaning Up...')
        self.gen_lib.clean_build()

        for b in self.buttons: b.setEnabled(True)
        self.StatusMsg.setText('Standby.')
        os.system("start " + self.export_dir)
