from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import requests

BASE_URL = "http://localhost:5000"


class VanzariProduseScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.setWindowTitle("Distribuție Vânzări Produse")
        self.setGeometry(100, 100, 800, 600)

        self.canvas = FigureCanvas(plt.figure())
        layout.addWidget(self.canvas)

        self.fetch_and_display_chart()

        self.setLayout(layout)

    def fetch_and_display_chart(self):
        """
            Fetch data from the backend API and display it as a pie chart
        """
        response = requests.get(f"{BASE_URL}/get_total_vanzari_produs")
        if response.status_code == 200:
            report_data = response.json()

            # Check if the data is list of dictionaries
            if isinstance(report_data, list) and len(report_data) > 0:
                self.plot_pie_chart(report_data)
            else:
                QMessageBox.warning(self, "No Data", "Nu există date disponibile pentru raport.")
       
        else:
            QMessageBox.critical(self, "Error", f"Nu s-au putut încărca datele raportului.\n{response.text}")
        
    def plot_pie_chart(self, data):
        """
            Create a pie chart from the fetched report data
        """
        # Prepare data for the pie chart
        product_names = [row['nume_produs'] + " " + row['Total vanzari produs'] for row in data]
        total_sales = [row['Total vanzari produs'] for row in data]

        # Create a pie chart
        ax = self.canvas.figure.add_subplot(111)
        ax.clear()

        # Plotting the pie chart
        wedges, texts, autotexts = ax.pie(
            total_sales,
            labels=product_names,
            autopct='%1.1f%%',
            startangle=90,
            colors=plt.cm.tab20.colors
        )

        # Styling
        ax.set_title("Distribuție Vânzări Produse")
        for autotext in autotexts:
            autotext.set_color('white')

        # Refresh the canvas
        self.canvas.draw()