from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import requests

BASE_URL = "http://localhost:5000"

class StupiBarChartScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.setWindowTitle("Compararea Numarului de Familii, Tratamente si Hraniri")
        self.setGeometry(100, 100, 800, 600)

        self.canvas = FigureCanvas(plt.figure())
        layout.addWidget(self.canvas)

        self.fetch_and_display_chart()

        self.setLayout(layout)

    def fetch_and_display_chart(self):
        """
        Fetch data from the backend API and display it as a bar chart
        """
        response = requests.get(f"{BASE_URL}/get_statistici_stupi")
        if response.status_code == 200:
            report_data = response.json()

            # Check if the data is a list of dictionaries
            if isinstance(report_data, list) and len(report_data) > 0:

                self.plot_bar_chart(report_data)
            else:
                QMessageBox.warning(self, "No Data", "Nu există date disponibile pentru raport.")
        else:
            QMessageBox.critical(self, "Error", f"Nu s-au putut încărca datele raportului.\n{response.text}")

    def plot_bar_chart(self, data):
        """
        Create a bar chart from the fetched report data
        """
        # Prepare data for the bar chart
        tip_stup = [f"{entry['TipStup']} - {entry['RasaRegina']}" for entry in data]
        numar_familii = [entry['NumarFamiliiStup'] for entry in data]
        numar_tratamente = [entry['numar_mediu_tratamente'] for entry in data]
        numar_hraniri = [entry['numar_mediu_hraniri'] for entry in data]

        # Set positions for X axis
        x = np.arange(len(tip_stup))

        # Width of the bars
        width = 0.25

        # Create a new subplot for the bar chart
        ax = self.canvas.figure.add_subplot(111)
        ax.clear()

        # Plotting the bars for the data (similar to plot_pie_chart)
        ax.bar(x - width, numar_familii, width, label='Numar Familii Stup', color='lightblue')
        ax.bar(x, numar_tratamente, width, label='Numar Mediu Tratamente', color='lightgreen')
        ax.bar(x + width, numar_hraniri, width, label='Numar Mediu Hraniri', color='lightcoral')

        # Adding details to the plot (labels, title, etc.)
        ax.set_xlabel('Cea mai comuna rasa de regina per tip de stup')
        ax.set_ylabel('Valori')
        ax.set_title('Comparare Numar de Familii, Tratamente si Hraniri')
        ax.set_xticks(x)
        ax.set_xticklabels(tip_stup)
        ax.legend()

        # Styling and layout adjustments
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Refresh the canvas (similar to plot_pie_chart)
        self.canvas.draw()
