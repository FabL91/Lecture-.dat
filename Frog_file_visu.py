import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog
from PyQt6.uic import loadUi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("frog_file.ui", self)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        if self.mplWidget.layout() is None:
            layout = QVBoxLayout()
            self.mplWidget.setLayout(layout)
        self.mplWidget.layout().addWidget(self.toolbar)
        self.mplWidget.layout().addWidget(self.canvas)

        self.openButton.clicked.connect(self.open_file)
        self.colonne1.stateChanged.connect(self.update_plot)
        self.colonne2.stateChanged.connect(self.update_plot)
        self.colonne3.stateChanged.connect(self.update_plot)
        self.colonne4.stateChanged.connect(self.update_plot)


    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open .dat file", "", "Data files (*.dat)")
        if filename:
            self.filename = filename
            try:
                self.data = np.loadtxt(filename)
                self.update_plot()
            except FileNotFoundError:
                print(f"Error: File '{filename}' not found.")
            except ValueError:
                print(f"Error: File '{filename}' contains invalid data. Make sure it's in numerical format with spaces or tabs as separators.")


    def update_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.grid(True)
        
        if self.filename:
            try:
                num_cols = self.data.shape[1]
                if num_cols < 4:
                    print(f"Error: Data file does not contain enough columns (at least 4 needed).")
                    return

                x_data = None
                y_data = None
                xlabel = ""
                ylabel = ""

                if self.colonne1.isChecked():
                    x_data = self.data[:,0]
                    xlabel = "Colonne 1"

                if self.colonne2.isChecked():
                    if x_data is not None:
                        y_data = self.data[:,1]
                        ylabel = "Colonne 2"
                    else:
                        x_data = self.data[:,1]
                        xlabel = "Colonne 2"

                if self.colonne3.isChecked():
                    if x_data is not None:
                        y_data = self.data[:,2]
                        ylabel = "Colonne 3"
                    else:
                        x_data = self.data[:,2]
                        xlabel = "Colonne 3"

                if self.colonne4.isChecked():
                    if x_data is not None:
                        y_data = self.data[:,3]
                        ylabel = "Colonne 4"
                    else:
                        x_data = self.data[:,3]
                        xlabel = "Colonne 4"



                if x_data is None or y_data is None:
                    print("Please select at least two columns.")
                    return

                ax.plot(x_data, y_data, marker='o', linestyle='-')
                ax.set_xlabel(xlabel)
                ax.set_ylabel(ylabel)
                ax.set_title(f"Data from file {self.filename}")
                self.canvas.draw()

            except IndexError:
                print("Error: Not enough columns in data.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
