import PySide6.QtWidgets
import sys
from gui import MainWindow
import PySide6
"""
main runs the GUI for the program where the rest of the program is handled
"""


def main():
    gui = PySide6.QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(gui.exec_())


if __name__ == "__main__":
    main()
