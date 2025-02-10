from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import squarify
import requests

BASE_URL = "http://localhost:5000" 

class ApicultoriTreemapScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.setWindowTitle("Treemap: Apicultori - Număr Interventii")
        self.setGeometry(100, 100, 800, 600)

        self.canvas = FigureCanvas(plt.figure())
        layout.addWidget(self.canvas)

        self.fetch_and_display_treemap()

        self.setLayout(layout)

    def fetch_and_display_treemap(self):
        """
        Fetch data from the backend API and display it as a treemap
        """
        response = requests.get(f"{BASE_URL}/get_data_apicultori")
        if response.status_code == 200:
            report_data = response.json()

            if isinstance(report_data, list) and len(report_data) > 0:
                self.plot_treemap(report_data)
            else:
                QMessageBox.warning(self, "No Data", "Nu există date disponibile pentru raport.")
        else:
            QMessageBox.critical(self, "Error", f"Nu s-au putut încărca datele raportului.\n{response.text}")

    def plot_treemap(self, data):
        """
        Create a treemap from the fetched report data
        """

        labels = [
            f"{entry['nume']} {entry['prenume']}\nNivel: {entry['nivel_experienta']}\nInterventii: {entry['numar_interventii']}\nMaestru: {entry['nume_maestru']}"
            for entry in data
        ]
        sizes = [entry['numar_interventii'] for entry in data]
        colors = ["green" if entry['nivel_experienta'] == "Expert" else "red" for entry in data]

        ax = self.canvas.figure.add_subplot(111)
        ax.clear()

        squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.7, ax=ax)

        ax.set_title("Treemap: Apicultori - Numar Interventii, Nivel de Experienta si Maestru")

        numar_interventii = [entry['numar_interventii'] for entry in data]
        numar_mediu_interventii = sum(numar_interventii) / len(numar_interventii)

        # Adăugarea numărului mediu de intervenții
        ax.text(0.95, 0.95, f'Numar Mediu Interventii: {numar_mediu_interventii:.2f}',
                horizontalalignment='right', verticalalignment='top', transform=ax.transAxes,
                fontsize=12, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

        ax.axis('off')

        self.canvas.draw()
