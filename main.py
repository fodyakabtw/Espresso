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

        self.add_or_change.clicked.connect(self.run)

    def run(self):
        self.second_window = Kapuchino()
        self.hide()
        self.second_window.show()


class Kapuchino(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.spisok = set()
        self.add_button.clicked.connect(self.add)
        self.change_button.clicked.connect(self.change)

    def add(self):
        if self.id1_edit.text() == '':
            self.statusBar().showMessage('Введите ID')
            return
        elif self.sort1_edit.text() == '':
            self.statusBar().showMessage('Введите название сорта')
            return
        elif self.obj1_edit.text() == '':
            self.statusBar().showMessage('Введите степень обжарки')
            return
        elif self.zern1_edit.text() == '':
            self.statusBar().showMessage('Введите молотый/в зернах')
            return
        elif self.opis1_edit.text() == '':
            self.statusBar().showMessage('Введите описание вкуса')
            return
        elif self.price1_edit.text() == '':
            self.statusBar().showMessage('Введите цену')
            return
        elif self.v1_edit.text() == '':
            self.statusBar().showMessage('Введите объем упаковки')
            return
        else:
            if self.sort1_edit.text() not in self.spisok:
                self.spisok.add(self.sort1_edit.text())
                try:
                    self.con = sqlite3.connect('coffee.sqlite')
                    self.cur = self.con.cursor()
                    self.cur.execute(
                        """INSERT INTO coffee (ID, sort_name, roast_degree, ground_or_whole, taste_description,
                         price, package_volume) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (int(self.id1_edit.text()), self.sort1_edit.text(), self.obj1_edit.text(),
                         self.zern1_edit.text(),
                         self.opis1_edit.text(), int(self.price1_edit.text()), int(self.v1_edit.text()),))
                    self.con.commit()
                    self.spisok.add(self.sort1_edit.text())
                    self.statusBar().showMessage('Данные успешно добавлены!')
                    self.con.close()
                except sqlite3.IntegrityError:
                    self.statusBar().showMessage('Кофе с таким айди уже занят!')
                except ValueError:
                    self.statusBar().showMessage('Айди, цена или объем не может быть текстом!')
            else:
                self.statusBar().showMessage('Кофе с таким сортом уже есть!')
                return

    def change(self):
        if self.id2_edit.text() == '':
            self.statusBar().showMessage('Введите ID изменяемого кофе!')
            return
        elif self.sort2_edit.text() == '':
            self.statusBar().showMessage('Введите название сорта')
            return
        elif self.obj2_edit.text() == '':
            self.statusBar().showMessage('Введите степень обжарки')
            return
        elif self.zern2_edit.text() == '':
            self.statusBar().showMessage('Введите молотый/в зернах')
            return
        elif self.opis2_edit.text() == '':
            self.statusBar().showMessage('Введите описание вкуса')
            return
        elif self.price2_edit.text() == '':
            self.statusBar().showMessage('Введите цену')
            return
        elif self.v2_edit.text() == '':
            self.statusBar().showMessage('Введите объем упаковки')
            return
        else:
            try:
                self.spisok.add(self.sort2_edit.text())
                self.con = sqlite3.connect('coffee.sqlite')
                self.cur = self.con.cursor()
                if self.sort2_edit.text() not in self.spisok:
                    self.cur.execute(
                        """UPDATE coffee SET sort_name = ?, roast_degree = ?, ground_or_whole = ?,
                         taste_description = ?, price = ?, package_volume = ? WHERE ID = ?""",
                        (self.sort2_edit.text(), self.obj2_edit.text(),
                         self.zern2_edit.text(),
                         self.opis2_edit.text(), int(self.price2_edit.text()), int(self.v2_edit.text()),
                         self.id2_edit.text(),))
                    self.con.commit()
                    self.spisok.add(self.sort2_edit.text())
                    self.statusBar().showMessage('Данные успешно обновлены!')
                    self.con.close()
                else:
                    self.statusBar().showMessage('Кофе с таким сортом уже существует!')
            except ValueError:
                self.statusBar().showMessage('Айди, цена или объем не может быть текстом!')

    def closeEvent(self, a0):
        self.first = Espresso()
        self.first.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Espresso()
    ex.show()
    sys.exit(app.exec_())
