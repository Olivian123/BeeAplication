from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QFormLayout, QCheckBox, QMessageBox, QComboBox
from PyQt5.QtCore import Qt
from datetime import date
import requests

BASE_URL = "http://localhost:5000"

class AddVanzareScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Form Fields
        self.nume_produs_dropdown = QComboBox()
        self.nume_produs_dropdown.setPlaceholderText("Selectează produsul")
        form_layout.addRow("Nume Produs:", self.nume_produs_dropdown)

        self.cantitate_ceruta_input = QLineEdit()
        self.cantitate_ceruta_input.setPlaceholderText("Cantitate Ceruta")
        form_layout.addRow("Cantitate Ceruta:", self.cantitate_ceruta_input)

        self.data_vanzare_label = QLabel(f"Data Vanzarii: {date.today().isoformat()}")
        form_layout.addRow(self.data_vanzare_label)

        # Add Form Layout to Main Layout
        layout.addLayout(form_layout)

        # Button pentru trimitere
        add_button = QPushButton("Adauga Vanzare")
        add_button.clicked.connect(self.add_vanzare)
        layout.addWidget(add_button)

        self.setLayout(layout)

        # Fetch product data and populate the dropdown
        self.fetch_products()

    def fetch_products(self):
        """
            Fetches the products from the API and populates the dropdown.
        """
        response = requests.get(f"{BASE_URL}/produs")

        if response.status_code == 201:
            products = response.json()

            # Populate dropdown list
            for product in products:
                product_name = f"{product['nume_produs']} (Cantitate: {product['cantitate']})"
                self.nume_produs_dropdown.addItem(product_name, userData=product['id_produs'])
        else:
            QMessageBox.critical(self, "Error", "Nu s-au putut încărca produsele.")

    def add_vanzare(self):
        """Trimite o cerere POST pentru a adăuga vânzarea."""
        nume_produs = self.nume_produs_dropdown.currentText().split("(")[0][:-1]
        cantitate_ceruta = self.cantitate_ceruta_input.text()

        if not nume_produs or not cantitate_ceruta:
            QMessageBox.critical(self, "Input Error", "Toate câmpurile sunt obligatorii!")
            return

        # Data
        data = {
            "nume_produs": nume_produs,
            "cantitate_ceruta": int(cantitate_ceruta)
        }

        response = requests.post(f"{BASE_URL}/vanzare", json=data)
        
        if response.status_code == 201:
            QMessageBox.information(self, "Success", "Vânzarea a fost adăugată cu succes!")
        else:
            QMessageBox.critical(self, "Error", f"Failed: {response.json().get('error', 'Error!')}")
