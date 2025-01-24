import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QFileDialog, QMessageBox, QSizePolicy
from PyQt6.uic import loadUi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import pandas as pd  # Import pandas for Excel saving



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("frog_file.ui", self)
        
        # Create a Figure instance
        self.figure = Figure()
        
        # Create two subplots
        self.ax1 = self.figure.add_subplot(211)
        self.ax2 = self.figure.add_subplot(212)
        # Create canvas
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        if self.mplWidget.layout() is None:
            layout = QVBoxLayout()
            self.mplWidget.setLayout(layout)
        self.mplWidget.layout().addWidget(self.toolbar)
        self.mplWidget.layout().addWidget(self.canvas)

        # Set the canvas to expand both horizontally and vertically
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.canvas.updateGeometry()

        # Connect the resize event of mplWidget to update the figure
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
        
    def on_mpl_resize(self, event):
        # This method will be called when mplWidget is resized
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
                QMessageBox.critical(self, "Error", f"File '{filename}' contains invalid data. Make sure it's in numerical format with spaces or tabs as separators.")
                
    def open_file_spectre(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Speck.dat file", "", "Data files (*.dat)")
        if filename:
            self.filename = filename
            try:
                self.data = np.loadtxt(filename)
                self.update_plot_spectre()
            except FileNotFoundError:
                QMessageBox.critical(self, "Error", f"File '{filename}' not found.")
            except ValueError:
                QMessageBox.critical(self, "Error", f"File '{filename}' contains invalid data. Make sure it's in numerical format with spaces or tabs as separators.")


    def update_plot(self):
        
        
        if self.filename:
            try:
                num_cols = self.data.shape[1]
                if num_cols < 2:  # Minimum 2 columns needed for plotting
                    QMessageBox.critical(self, "Error", "Data file must have at least two columns.")
                    return

                x_data = None
                y_data = None

                #Simplified column selection logic:
                checked_columns = [
                    self.colonne1.isChecked(),
                    self.colonne2.isChecked(),
                    self.colonne3.isChecked(),
                    self.colonne4.isChecked(),
                    self.colonne5.isChecked()
                ]
                
                selected_cols = np.where(np.array(checked_columns))[0]

                if len(selected_cols) >= 2:
                    x_data = self.data[:, selected_cols[0]]
                    y_data = self.data[:, selected_cols[1]]
                    
                    if len(selected_cols) > 2: #more than 2 columns selected. use 1st 2.
                        print("Warning: More than 2 columns selected. Only using the first two.")
                

                    self.x_data = x_data #store for saving
                    self.y_data = y_data #store for saving
                    
                    # Clear previous plots
                    self.ax1.clear()
                    


                    self.ax1.plot(x_data, y_data, marker='o', linestyle='-')
                    self.ax1.set_xlabel("Time (fs)")
                    self.ax1.set_ylabel("Intensity") #generic label for better practice.
                    self.ax1.set_title(f"Data from file {self.filename}")
                    
                              
                
                    self.canvas.draw()
                
                elif len(selected_cols) < 2:
                    QMessageBox.critical(self, "Error", "Please select at least two columns.")
                    return

            except IndexError:
                QMessageBox.critical(self, "Error", "Not enough columns in data.")
                
                
    def update_plot_spectre(self):
        
        
        if self.filename:
            try:
                num_cols = self.data.shape[1]
                if num_cols < 2:  # Minimum 2 columns needed for plotting
                    QMessageBox.critical(self, "Error", "Data file must have at least two columns.")
                    return

                x_data = None
                y_data = None

                #Simplified column selection logic:
                checked_columns = [
                    self.colonne1.isChecked(),
                    self.colonne2.isChecked(),
                    self.colonne3.isChecked(),
                    self.colonne4.isChecked(),
                    self.colonne5.isChecked()
                ]
                
                selected_cols = np.where(np.array(checked_columns))[0]

                if len(selected_cols) >= 2:
                    x_data = self.data[:, selected_cols[0]]
                    y_data = self.data[:, selected_cols[1]]
                    
                    if len(selected_cols) > 2: #more than 2 columns selected. use 1st 2.
                        print("Warning: More than 2 columns selected. Only using the first two.")
                

                    self.x_data = x_data #store for saving
                    self.y_data = y_data #store for saving
                    
                    # Clear previous plots
                    self.ax2.clear()

                    
                    
                    #Example of adding a second plot (replace with your desired plot)
                    self.ax2.plot(x_data, y_data, 'r-', label='Spectre') #plot something on ax2
                    self.ax2.set_xlabel("Longueur d'onde (nm)")
                    self.ax2.set_ylabel("Intensity")
                    self.ax2.set_title(f"Data from file {self.filename}")
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
                    QMessageBox.information(self, "Success", f"Data saved to {filename}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"An error occurred while saving: {e}")
        else:
            QMessageBox.warning(self, "Warning", "No data to save. Please open a file and select columns.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
