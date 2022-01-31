# GUI imports
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
# function imports
from functions import frame1, frame2, frame3, frame4, grid

# initialize GUI application
app = QApplication(sys.argv)

# window and settings
window = QWidget()
window.setWindowTitle("Welcome to AI Therapist!!!")
window.setFixedWidth(1000)
# place window in (x,y) coordinates
# window.move(100, 70)
window.setStyleSheet("background: #161219;")

# display frame 1
frame1()

window.setLayout(grid)
window.show()

try:
    sys.exit(app.exec())  # terminate the app
except SystemExit:
    print('Closing Window...')
