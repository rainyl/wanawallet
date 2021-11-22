'''
Description: the gui program
Author: Rainyl
Date: 2021-11-21 23:06:14
LastEditTime: 2021-11-22 12:00:30
'''
import os
from datetime import datetime
from pathlib import Path
from wanawalletUI import Ui_MainWindow
from PySide6.QtWidgets import (QMainWindow, QFileDialog, QMessageBox,
    QTableWidgetItem, QApplication)
from PySide6.QtCore import QFile, Slot, Signal, QObject, Qt

from utils import washer, getRecords, insert2Na, TYPE_HASH
from config import DEFAULT_THEME

class WANawallet(QMainWindow, Ui_MainWindow):
    billFiles = None
    dbfile = None
    allRecords = []
    timeFormat = "%Y-%m-%d %H:%M:%S"
    def __init__(self, parent=None):
        super(WANawallet, self).__init__(parent=parent)
        self.setupUi(self)
        self.setSignals()
        self.setTheme()
        self.moveWindowLocation()

    def moveWindowLocation(self):
        screen = self.screen().availableSize()
        widget = self.size()
        centerX = (screen.width() - widget.width()) / 2
        centerY = (screen.height() - widget.height()) / 2
        self.move(centerX, centerY)

    def setTheme(self, theme=DEFAULT_THEME):
        if os.path.exists(theme):
            with open(theme, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())

    def setSignals(self):
        self.btnInput.clicked.connect(self.onBtnInputClicked)
        self.btnOutput.clicked.connect(self.onBtnOutputClicked)
        self.btnConvert.clicked.connect(self.onBtnConvertClicked)

    @Slot()
    def onBtnInputClicked(self):
        files = QFileDialog().getOpenFileNames(self, caption="Select Files", dir=".", filter="*.csv")[0]
        if files:
            self.billFiles = files
            self.getRecords()
            self.showTable()
            self.tbrowserInput.setText("\n".join(files))
        print(files)

    @Slot()
    def onBtnOutputClicked(self):
        dbfile = QFileDialog().getOpenFileName(
            self, 
            caption="Select your backuped database file", 
            dir=".", 
            filter="SQLite3(*.db *.sqlite3);;All files(*.*)"
        )[0]
        if Path(dbfile).exists:
            self.dbfile = dbfile
            self.tbrowserOutput.setText(dbfile)

    @Slot()
    def onBtnConvertClicked(self):
        if not (self.dbfile and self.allRecords):
            QMessageBox(
                QMessageBox.Warning,
                "Warning",
                "Please select your database file first!",
                buttons=QMessageBox.Ok,
                parent=self
            ).show()
            return
        records = []
        for row in range(self.tableBills.rowCount()):
            money = self.tableBills.item(row, 0).data(Qt.EditRole)
            remark = self.tableBills.item(row, 3).data(Qt.EditRole)
            time = self.tableBills.item(row, 2).data(Qt.EditRole)
            time = datetime.strptime(time, self.timeFormat).timestamp()
            ctime = datetime.now().timestamp()
            recordType = self.tableBills.item(row, 4).data(Qt.EditRole)
            assetId = self.tableBills.item(row, 5).data(Qt.EditRole)
            tmp = [
                int(money*100),
                remark,
                int(time*1000),
                int(ctime*1000),
                recordType,
                assetId,
            ]
            records.append(tmp)
        self.allRecords = records
        r = insert2Na(self.dbfile, records)
        if r["status"]:
            QMessageBox(
                QMessageBox.Information,
                "Success",
                f"Save to {self.dbfile} success!",
                buttons=QMessageBox.Ok,
                parent=self
            ).show()
        else:
            QMessageBox(
                QMessageBox.Critical,
                "Fail",
                f"Save to {self.dbfile} fail!\n{r['msg']}",
                buttons=QMessageBox.Ok,
                parent=self
            ).show()
        # print(records)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            rowranges = self.tableBills.selectedRanges()
            while rowranges:
                row = rowranges[0]
                # print(f"row:{row}")
                for r in range(row.rowCount()):
                    self.tableBills.removeRow(row.topRow())
                    # print(f"removed row: {row.topRow()}")
                rowranges = self.tableBills.selectedRanges()
            return super().keyPressEvent(event)
        else:
            return super().keyPressEvent(event)

    def getRecords(self):
        for bill in self.billFiles:
            path = Path(bill)
            kind = "alipay" if path.name.startswith("alipay") else "wechat"
            df = washer(bill, kind)
            records = getRecords(df)
            self.allRecords.extend(records)

    def showTable(self):
        self.tableBills.setRowCount(0)
        for i, row in enumerate(self.allRecords):
            self.tableBills.insertRow(i)
            itemMoney = QTableWidgetItem()
            itemMoney.setData(Qt.EditRole, row[0]/100)
            self.tableBills.setItem(i, 0, itemMoney)  # money
            self.tableBills.setItem(i, 1, QTableWidgetItem("WeChat" if row[4] in [36, 38] else "AliPay"))  # source
            self.tableBills.setItem(
                i, 
                2, 
                QTableWidgetItem(
                    datetime.fromtimestamp(row[2]/1000).strftime(self.timeFormat)
                )
            )  # time
            self.tableBills.setItem(i, 3, QTableWidgetItem(str(row[1])))  # remark
            self.tableBills.setItem(i, 4, QTableWidgetItem(str(row[4])))  # type
            self.tableBills.setItem(i, 5, QTableWidgetItem(str(row[5])))  # assets


    
class PreWorker(QObject):
    finished = Signal(object)

    def __init__(self,):
        super(PreWorker, self).__init__()

    @Slot()
    def run(self):
        pass

