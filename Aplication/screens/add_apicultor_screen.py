from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QFormLayout, QMessageBox, QComboBox
from datetime import date
import requests

BASE_URL = "http://localhost:5000"

class AddApicultorScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Use a Form Layout for Alignment
        form_layout = QFormLayout()

        self.nume_input = QLineEdit()
        self.nume_input.setPlaceholderText("Nume")
        form_layout.addRow("Nume:", self.nume_input)

        self.prenume_input = QLineEdit()
        self.prenume_input.setPlaceholderText("Prenume")
        form_layout.addRow("Prenume:", self.prenume_input)

        self.rol_input = QLineEdit()
        self.rol_input.setPlaceholderText("Rol")
        form_layout.addRow("Rol:", self.rol_input)

        # Dropdown for Maestru
        self.maestru_combo = QComboBox()
        self.maestru_combo.addItem("Selectează Maestrul")
        form_layout.addRow("Maestru:", self.maestru_combo)
        
        # Today's Date
        self.data_angajarii_label = QLabel(f"Data Angajării: {date.today().isoformat()}")
        form_layout.addRow(self.data_angajarii_label)

        # Add Form Layout to Main Layout
        layout.addLayout(form_layout)

        # Add Button
        add_button = QPushButton("Add Apicultor")
        add_button.clicked.connect(self.add_apicultor)
        layout.addWidget(add_button)

        self.setLayout(layout)

        # Fetch the list of potential maestri
        self.fetch_maestri()

    def fetch_maestri(self):
        """
            Fetch the list of beekeepers who can be selected as 'maestru'.
        """
        response = requests.get(f"{BASE_URL}/apicultori")

        if response.status_code == 201:
            apicultori = response.json()
            for apicultor in apicultori:
                # Populate combo box with maestri
                self.maestru_combo.addItem(f"{apicultor['nume']} {apicultor['prenume']}", apicultor['id_apicultor'])
        else:
            QMessageBox.critical(self, "Error", "Failed to fetch maestri list.")

    def add_apicultor(self):
        """
            Send a POST request to add a new bee keeper.
        """
        nume = self.nume_input.text()
        prenume = self.prenume_input.text()
        rol = self.rol_input.text()
        id_maestru = self.maestru_combo.currentData()

        if not nume or not prenume or not rol:
            QMessageBox.critical(self, "Input Error", "Toate câmpurile sunt obligatorii!")
            return
        
        if id_maestru is None:
            QMessageBox.critical(self, "Input Error", "Trebuie să selectezi un maestru!")
            return

        data = {"nume": nume, "prenume": prenume, "rol": rol, "id_maestru": id_maestru}

        response = requests.post(f"{BASE_URL}/apicultori", json=data)
        
        if response.status_code == 201:
            QMessageBox.information(self, "Success", "Apicultor adaugat cu succes!")
        else:
            QMessageBox.critical(
                self, "Error", "Failed!"
            )
