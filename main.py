# Tuzuvchi: Otaboboyev Akmal
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
from PyQt5 import uic
import configparser
import sys
import datetime


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("MainWindow3.ui", self)
        price = self.get_price()
        self.price_a5.setText(str(price[0]))
        self.price_a4.setText(str(price[1]))
        self.price_stepler_a5.setText(str(price[2]))
        self.price_stepler_a4.setText(str(price[3]))
        self.price_pereplyot_a5.setText(str(price[4]))
        self.price_pereplyot_a4.setText(str(price[5]))

        self.price_save.clicked.connect(lambda: self.save())

        # self.btnEnter.clicked.connect(lambda: self.solve())
        self.btnCopy.clicked.connect(lambda: self.copy())
        self.btnAbout.clicked.connect(lambda: self.about())
        self.btnAdd.clicked.connect(lambda: self.addItems())
        self.btnClear.clicked.connect(lambda: self.clearForm())
        self.btnRemove.clicked.connect(lambda: self.objRemove())
        self.dataAvans.setCurrentIndex(2)

    def objRemove(self):
        self.jadval.removeRow(self.jadval.currentRow())
        self.solve()

    def clearForm(self, tozalash=True):
        self.dataName.setText("")
        self.dataPages.setText("")
        self.dataFormat.setCurrentIndex(0)
        self.dataTuri.setCurrentIndex(0)
        self.dataAvans.setCurrentIndex(2)
        self.dataSoni.setValue(1)
        if tozalash:
            for row in range(self.jadval.rowCount()-1, -1, -1):
                self.jadval.removeRow(row)
            self.result_price.setText("0")
            self.result_avans.setText("0")

    def addItems(self):
        price = self.get_price()
        prices = {"A5": price[0], "A4": price[1], "Stepler": {
            "A5": price[2], "A4": price[3]}, "Pereplyot": {"A5": price[4], "A4": price[5]}}
        summa = (int(self.dataPages.text())*int(prices[self.dataFormat.currentText()])+int(
            prices[self.dataTuri.currentText()][self.dataFormat.currentText()]))*self.dataSoni.value()
        sana = datetime.date.today().strftime("%d.%m.%Y")
        data = [
            str(sana),
            str(self.dataName.text()),
            str(self.dataPages.text()),
            str(self.dataFormat.currentText()),
            str(self.dataTuri.currentText()),
            str(self.dataSoni.value()),
            str(self.dataAvans.currentText()),
            str(summa)
        ]
        row = self.jadval.rowCount()
        self.jadval.setRowCount(row+1)
        self.jadval.setColumnCount(self.jadval.columnCount())
        self.jadval.setItem(row, 0, QTableWidgetItem(data[0]))
        self.jadval.setItem(row, 1, QTableWidgetItem(data[1]))
        self.jadval.setItem(row, 2, QTableWidgetItem(data[2]))
        self.jadval.setItem(row, 3, QTableWidgetItem(data[3]))
        self.jadval.setItem(row, 4, QTableWidgetItem(data[4]))
        self.jadval.setItem(row, 5, QTableWidgetItem(data[5]))
        self.jadval.setItem(row, 6, QTableWidgetItem(data[6]))
        self.jadval.setItem(row, 7, QTableWidgetItem(data[7]))
        self.solve()
        self.clearForm(False)

    def solve(self):
        # n = int(self.dataPages.text()) if self.dataPages.text().isdigit() else 0
        # if n > 0:
        summ = 0
        avans = 0
        # print(self.jadval.item(0, 6).text())
        for row in range(self.jadval.rowCount()):
            n = int(self.jadval.item(row, 7).text())
            summ += n
            avans += n*int(self.jadval.item(row, 6).text()[:-1])/100
        self.result_price.setText(f"{summ:,d}".replace(",","."))
        self.result_avans.setText(f"{int(avans):,d}".replace(",","."))

    def about(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        text = '''Bu dastur \"boss print\" uchun maxsus ishlab chiqilgan\nDastur versiyasi: V3.18.04.2022 \n\nTuzuvchi: Otaboboyev Akmal\nE-mail: akmal.otaboboyev@gmail.com\n\n\nBu dastur python dasturlash tilida yozilgan'''
        msg.setText(text)
        msg.setWindowTitle("Dastur haqida")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def save(self):
        config = configparser.ConfigParser()
        config["Price"] = {
            "price_a5": int(self.price_a5.text()),
            "price_a4": int(self.price_a4.text()),
            "price_stepler_a5": int(self.price_stepler_a5.text()),
            "price_stepler_a4": int(self.price_stepler_a4.text()),
            "price_pereplyot_a5": int(self.price_pereplyot_a5.text()),
            "price_pereplyot_a4": int(self.price_pereplyot_a4.text())}
        with open("prices.ini", "w") as configdata:
            config.write(configdata)

    def get_price(self):
        config = configparser.ConfigParser()
        if config.read("prices.ini"):
            prices = (
                int(config["Price"]["price_a5"]),
                int(config["Price"]["price_a4"]),
                int(config["Price"]["price_stepler_a5"]),
                int(config["Price"]["price_stepler_a4"]),
                int(config["Price"]["price_pereplyot_a5"]),
                int(config["Price"]["price_pereplyot_a4"])
            )
        else:
            prices = (0, 0, 0, 0, 0, 0)
        return prices

    def copy(self):
        text = ""
        for row in range(self.jadval.rowCount()):
            text += "Sana: {}\nKitob nomi: {}\nSahifalar soni: {}\nFormati: {}\nTuri: {}\nBuyurtma soni: {}\nOldindan to'lov miqdori: {}\nSumma: {} so'm\n\n".format(
                self.jadval.item(row, 0).text(),
                self.jadval.item(row, 1).text(),
                self.jadval.item(row, 2).text(),
                self.jadval.item(row, 3).text(),
                self.jadval.item(row, 4).text(),
                self.jadval.item(row, 5).text(),
                self.jadval.item(row, 6).text(),
                self.jadval.item(row, 7).text())

        text += "-"*20+"\nJami summa: {} so'm\nOldindan to'lov: {} so'm".format(
            self.result_price.text(), self.result_avans.text())
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(text, mode=cb.Clipboard)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
