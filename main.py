import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem
from PyQt5 import uic

conn = sqlite3.connect('coffee.sqlite')
cursor = conn.cursor()


class Espresso(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()

        self.cof = self.cur.execute("""SELECT * FROM coffee""").fetchall()

        print(self.cof)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.verticalHeader().setDefaultSectionSize(20)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(40)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents)
        self.tableWidget.setSortingEnabled(True)

        for i, row in enumerate(self.cof):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Espresso()
    ex.show()
    sys.exit(app.exec_())
