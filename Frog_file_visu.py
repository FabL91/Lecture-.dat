import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog, QMessageBox, QSizePolicy
from PyQt6.uic import loadUi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("frog_file.ui", self)
        self.figure = Figure()
        self.ax1 = self.figure.add_subplot(211)
        self.ax2 = self.figure.add_subplot(212)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        if self.mplWidget.layout() is None:
            layout = QVBoxLayout()
            self.mplWidget.setLayout(layout)
        self.mplWidget.layout().addWidget(self.toolbar)
        self.mplWidget.layout().addWidget(self.canvas)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.canvas.updateGeometry()
        self.mplWidget.resizeEvent = self.on_mpl_resize
        self.openSpeckButton.clicked.connect(self.open_file_spectre)
        self.openButton.clicked.connect(self.open_file)
        self.saveButton.clicked.connect(self.save_data)
        self.colonne1.stateChanged.connect(self.update_plot)
        self.colonne2.stateChanged.connect(self.update_plot)
        self.colonne3.stateChanged.connect(self.update_plot)
        self.colonne4.stateChanged.connect(self.update_plot)
        self.colonne5.stateChanged.connect(self.update_plot)
        self.filename = None  
        self.x_data = None
        self.y_data = None
        self.longueurOnde.stateChanged.connect(self.update_plot_spectre)
        self.intensiteSpectrale.stateChanged.connect(self.update_plot_spectre)
        self.phaseSpectrale.stateChanged.connect(self.update_plot_spectre)
        self.saveSpeckButton.clicked.connect(self.save_data_spectre)
        self.colonne1.setChecked(True)
        self.colonne2.setChecked(True)
        self.longueurOnde.setChecked(True)
        self.intensiteSpectrale.setChecked(True)
        
    def on_mpl_resize(self, event):
        self.figure.tight_layout()
        self.canvas.draw()    
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Ek.dat file", "", "Data files (*.dat)")
        if filename:
            self.filename = filename
            try:
                self.data = np.loadtxt(filename)
                self.update_plot()
            except FileNotFoundError:
                QMessageBox.critical(self, "Error", f"File '{filename}' not found.")
            except ValueError:
                QMessageBox.critical(self, "Error", f"File '{filename}' contains invalid data.")
    def open_file_spectre(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Speck.dat file", "", "Data files (*.dat)")
        if filename:
            self.filename = filename
            try:
                self.data_spectre = np.loadtxt(filename)
                self.update_plot_spectre()
            except FileNotFoundError:
                QMessageBox.critical(self, "Error", f"File '{filename}' not found.")
            except ValueError:
                QMessageBox.critical(self, "Error", f"File '{filename}' contains invalid data.")
    def update_plot(self):
        if self.filename:
            try:
                num_cols = self.data.shape[1]
                if num_cols < 2:
                    QMessageBox.critical(self, "Error", "Data file must have at least two columns.")
                    return
                checked_columns = [
                    self.colonne1.isChecked(),
                    self.colonne2.isChecked(),
                    self.colonne3.isChecked(),
                    self.colonne4.isChecked(),
                    self.colonne5.isChecked()
                ]
                selected_cols = np.where(np.array(checked_columns))[0]
                if len(selected_cols) < 2:
                    QMessageBox.critical(self, "Error", "Please select at least two columns.")
                    return
                x_data = self.data[:, selected_cols[0]]
                y_data = self.data[:, selected_cols[1]]
                
                self.x_data = x_data
                self.y_data = y_data
                z_data = None
                if len(selected_cols) >= 3:
                    z_data = self.data[:, selected_cols[2]]
                    if len(selected_cols) > 3:
                        print("Warning: More than 3 columns selected. Only using the first three.")
                elif len(selected_cols) == 2:
                    print("Warning: Only two columns selected. No z-axis data.")
                self.ax1.clear()
                
                self.ax1.plot(x_data, y_data, linestyle='-', label='Intensité')
                self.ax1.set_xlabel("Temps (fs)")
                self.ax1.set_ylabel("Intensité", color='blue')
                self.ax1.tick_params(axis='y', labelcolor='blue')
                
                if z_data is not None:
                    ax2 = self.ax1.twinx()
                    ax2.plot(x_data, z_data, linestyle=':', color='red', label='Phase')
                    ax2.set_ylabel("Phase Data (Units?)", color='red')
                    ax2.tick_params(axis='y', labelcolor='red')
                handles1, labels1 = self.ax1.get_legend_handles_labels()
                
                if z_data is not None:
                    handles2, labels2 = ax2.get_legend_handles_labels()
                    handles = handles1 + handles2
                    labels = labels1 + labels2
                    self.ax1.legend(handles, labels, loc='best')
                else:
                    self.ax1.legend(handles1, labels1, loc='best')
                    
                self.ax1.set_title(f"Data from file {self.filename}")
                self.canvas.draw()
                
            except IndexError:
                QMessageBox.critical(self, "Error", "Not enough columns in data.")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
                
    def update_plot_spectre(self):
        if self.filename:
            try:
                num_cols = self.data_spectre.shape[1]
                if num_cols < 2:
                    QMessageBox.critical(self, "Error", "Data file must have at least two columns.")
                    return
                checked_columns = [
                    self.longueurOnde.isChecked(),
                    self.intensiteSpectrale.isChecked(),
                    self.phaseSpectrale.isChecked()
                ]
                selected_cols = np.where(np.array(checked_columns))[0]
                if len(selected_cols) >= 2:
                    x_data_spectre = self.data_spectre[:, selected_cols[0]]
                    y_data_spectre = self.data_spectre[:, selected_cols[1]]
                    if len(selected_cols) > 2:
                        print("Warning: More than 2 columns selected. Only using the first two.")
                    self.x_data_spectre = x_data_spectre
                    self.y_data_spectre = y_data_spectre
                    self.ax2.clear()
                    self.ax2.plot(x_data_spectre, y_data_spectre, 'r-', label='Spectre')
                    self.ax2.set_xlabel("Longueur d'onde (nm)")
                    self.ax2.set_ylabel("Intensity")
                    self.ax2.set_title("Data from file ")
                    self.ax2.legend()
                    self.canvas.draw()
                elif len(selected_cols) < 2:
                    QMessageBox.critical(self, "Error", "Please select at least two columns.")
                    return
            except IndexError:
                QMessageBox.critical(self, "Error", "Not enough columns in data.")
    def save_data(self):
        if self.x_data is not None and self.y_data is not None:
            filename, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "Excel files (*.xlsx)")
            if filename:
                try:
                    df = pd.DataFrame({'x_data': self.x_data, 'y_data': self.y_data})
                    df.to_excel(filename, index=False)
                    QMessageBox.information(self, "Success", f"Les données du champs E(t) reconstruit sont sauvegardées à {filename}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred while saving: {e}")
        else:
            QMessageBox.warning(self, "Warning", "No data to save.")
    def save_data_spectre(self):
        if self.x_data_spectre is not None and self.y_data_spectre is not None:
            filename, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "Excel files (*.xlsx)")
            if filename:
                try:
                    df = pd.DataFrame({'x_data': self.x_data_spectre, 'y_data': self.y_data_spectre})
                    df.to_excel(filename, index=False)
                    QMessageBox.information(self, "Success", f"Les données du spectres reconstruit sont sauvegardées à{filename}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred while saving: {e}")
        else:
            QMessageBox.warning(self, "Warning", "No data to save.")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
