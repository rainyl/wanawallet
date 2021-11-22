'''
Description: main loop
Author: Rainyl
Date: 2021-11-21 23:08:06
LastEditTime: 2021-11-22 16:53:03
'''
import sys
from wanawallet import WANawallet
from PySide6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    mainWindow = WANawallet()
    mainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
