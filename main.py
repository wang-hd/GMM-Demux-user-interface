import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QFileDialog, QTextEdit, QTextBrowser
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from newui import Ui_MainWindow
from gmm import main

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("open file dialog")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.browse.clicked.connect(self.open)
        self.ui.browse_skip.clicked.connect(self.open_skip)
        self.ui.browse_output.clicked.connect(self.open_output)
        self.ui.browse_full.clicked.connect(self.open_full)
        self.ui.browse_simplified.clicked.connect(self.open_simplified)
        self.ui.browse_examine.clicked.connect(self.open_examine)
        self.ui.plot.clicked.connect(self.plot_select)
        self.ui.Output.clicked.connect(self.show_output)
        self.show()

    def open(self):
        path = QFileDialog.getExistingDirectory(None, 'Open a file', 'C:/')
        if path != ('', ''):
            print("File path : "+ path)
            self.ui.path.setText(str(path))

    def open_skip(self):
        path = QFileDialog.getExistingDirectory(None, 'Open a file', 'C:/')
        if path != ('', ''):
            print("File path : "+ path)
            self.ui.skip_path.setText(str(path))

    def open_output(self):
        path = QFileDialog.getExistingDirectory(None, 'Open a file', 'C:/')
        if path != ('', ''):
            print("File path : "+ path)
            self.ui.output_path.setText(str(path))

    def open_full(self):
        path = QFileDialog.getExistingDirectory(None, 'Open a file', 'C:/')
        if path != ('', ''):
            print("File path : "+ path)
            self.ui.full_path.setText(str(path))

    def open_simplified(self):
        path = QFileDialog.getExistingDirectory(None, 'Open a file', 'C:/')
        if path != ('', ''):
            print("File path : "+ path)
            self.ui.simplified_path.setText(str(path))

    def open_examine(self):
        path = QFileDialog.getExistingDirectory(None, 'Open a file', 'C:/')
        if path != ('', ''):
            print("File path : "+ path)
            self.ui.examine_path.setText(str(path))

    def file_select(self):
        path = QFileDialog.getOpenFileName(self, 'Open a file', '',
                                           'All Files (*.*)')
        if path != ('', ''):
            print("File path : " + path[0])
            self.ui.skip.setText(str(path[0]))


    def plot_select(self):
        if self.ui.scatter.isChecked():
            self.plot_scatter()
        else:
            self.plot_distribution()


    def plot_scatter(self):
        df = pd.read_csv(self.ui.path.toPlainText() + '/testdata.csv')
        x_data = df['x_data']
        y_data = df['y_data']
        plt.scatter(x_data, y_data)
        plt.title('Scatter Plot')
        plt.xlabel("x_label")
        plt.ylabel("y_label")
        plt_path = self.ui.path.toPlainText() + '/tmp.png'
        plt.savefig(plt_path)
        self.plot_window = Plot(plt_path)
        self.plot_window.show()
        os.remove(plt_path)


    def plot_distribution(self):
        df = pd.read_csv(self.ui.path.toPlainText() + '/distdata.csv')
        sns.displot(df)
        plt.xlabel("x_label")
        plt.ylabel("y_label")
        plt_path = self.ui.path.toPlainText() + '/tmp.png'
        plt.savefig(plt_path)
        self.plot_window = Plot(plt_path)
        self.plot_window.show()
        os.remove(plt_path)


    def show_output(self):
        command = 'GMM-demux '  + self.ui.path.toPlainText() + ' HTO_1,HTO_2,HTO_3,HTO_4'
        if self.ui.skip.isChecked():
            command += ' -k '
            command += self.ui.skip_path.toPlainText()
        if self.ui.output.isChecked():
            command += ' -o '
            command += self.ui.output_path.toPlainText()
        if self.ui.full.isChecked():
            command += ' -f '
            command += self.ui.full_path.toPlainText()
        if self.ui.simplified.isChecked():
            command += ' -s '
            command += self.ui.simplified_path.toPlainText()
        if self.ui.examine.isChecked():
            command += ' -e '
            command += self.ui.examine_path.toPlainText()
        if self.ui.extract.isChecked():
            command += ' -x '
            command += self.ui.extract_input.toPlainText()
        if self.ui.threshold.isChecked():
            command += ' -t '
            command += self.ui.threshold_input.toPlainText()
        if self.ui.summary.isChecked():
            command += ' -u '
            command += self.ui.summary_input.toPlainText()
        if self.ui.report.isChecked():
            command += ' -r '
            command += self.ui.report_input.toPlainText()
        if self.ui.ambiguous.isChecked():
            command += ' -a '
            command += self.ui.ambiguous_input.toPlainText()
        if self.ui.csv.isChecked():
            command += ' -c '
        print(command)
        result = main(command)
        print(result)
        self.child_window = Child(result)
        self.child_window.show()


class Child(QWidget):
    def __init__(self, result):
        super(Child, self).__init__()
        self.resize(1000, 700)
        self.setWindowTitle("Result")
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(result)


class Plot(QWidget):
    def __init__(self, plt_path):
        super(Plot, self).__init__()
        self.resize(1000, 700)
        self.setWindowTitle("Result")
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setPixmap(QPixmap(plt_path))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # loading interface
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap('1.png'))
    splash.show()
    splash.showMessage('Loading...')
    splash.close()

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())