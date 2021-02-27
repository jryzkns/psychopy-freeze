from PyQt5.QtWidgets import QApplication
from psychopyfreezeapp import PsychopyFreezeApp
import sys

if __name__ == '__main__':
    m = QApplication(sys.argv)
    app = PsychopyFreezeApp()
    app.show()
    sys.exit(m.exec_())
