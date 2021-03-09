import sys
from PyQt5 import QtWidgets, uic
import requests

# Read the UI file that QtDesigner spit out
qtcreator_file = "gui.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)

# Pulls currency exchange table from random free API I found online
response = requests.get('https://api.exchangeratesapi.io/latest').json()
currencies = sorted(list(response['rates'].keys()))


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.inputCurrency.addItems(currencies)
        self.outputCurrency.addItems(currencies)

        # All the buttons and input boxes
        self.swapButton.clicked.connect(self.swap_values)
        self.inputBox.valueChanged.connect(self.convert_currency)
        self.inputCurrency.currentIndexChanged.connect(self.convert_currency)
        self.outputCurrency.currentIndexChanged.connect(self.convert_currency)

    # Swap currencies when switch button is pressed
    def swap_values(self):
        inputcurr = int(self.inputCurrency.currentIndex())
        outputcurr = int(self.outputCurrency.currentIndex())
        self.outputCurrency.setCurrentIndex(inputcurr)
        self.inputCurrency.setCurrentIndex(outputcurr)

    # Do the actual conversion
    def convert_currency(self):
        value = self.inputBox.value()
        inputcurr = str(self.inputCurrency.currentText())
        outputcurr = str(self.outputCurrency.currentText())
        inputrate = response['rates'][inputcurr]
        outputrate = response['rates'][outputcurr]
        result = (value / inputrate) * outputrate
        result = str(round(result, 3))
        self.outputBox.setText(result)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setFixedSize(384, 216)
    window.show()
    sys.exit(app.exec_())
