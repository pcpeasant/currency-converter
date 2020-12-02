import sys
from PyQt5 import QtWidgets, uic
import requests

qtcreator_file = "currencyconvertergui.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

response = requests.get('https://api.exchangeratesapi.io/latest').json()
currencys = sorted(list(response['rates'].keys()))


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.inputCurrency.addItems(currencys)
        self.outputCurrency.addItems(currencys)

        self.swapButton.clicked.connect(self.swap_values)
        self.inputBox.valueChanged.connect(self.convert_currency)
        self.inputCurrency.currentIndexChanged.connect(self.convert_currency)
        self.outputCurrency.currentIndexChanged.connect(self.convert_currency)

    def swap_values(self):
        inputcurr = int(self.inputCurrency.currentIndex())
        outputcurr = int(self.outputCurrency.currentIndex())
        self.outputCurrency.setCurrentIndex(inputcurr)
        self.inputCurrency.setCurrentIndex(outputcurr)

    def convert_currency(self):
        value = self.inputBox.value()
        inputcurr = str(self.inputCurrency.currentText())
        outputcurr = str(self.outputCurrency.currentText())
        inputrate = response['rates'][inputcurr]
        outputrate = response['rates'][outputcurr]
        result = (value / inputrate) * outputrate
        result = str(round(result, 2))
        self.outputBox.setText(result)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setFixedSize(384, 216)
    window.show()
    sys.exit(app.exec_())
