from PySide6.QtWidgets import QMainWindow
import sys
import gui
from gui import MainWindow, SecondWindow, ThirdWindow, finalWindow
import PySide6

def main():
    gui = PySide6.QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(gui.exec_())

if __name__ == "__main__":
    main()
