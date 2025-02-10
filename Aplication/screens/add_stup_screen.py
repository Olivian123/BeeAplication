from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QMessageBox
from datetime import date
import requests

BASE_URL = "http://localhost:5000"

class AddStupScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        # Form Fields
        self.tip_input = QLineEdit()
        self.tip_input.setPlaceholderText("Tip Stup")
        form_layout.addRow("Tip Stup:", self.tip_input)

        self.numar_rame_input = QLineEdit()
        self.numar_rame_input.setPlaceholderText("Numar Rame")
        form_layout.addRow("Numar Rame:", self.numar_rame_input)

        self.dimensiuni_input = QLineEdit()
        self.dimensiuni_input.setPlaceholderText("Dimensiuni")
        form_layout.addRow("Dimensiuni:", self.dimensiuni_input)

        self.material_input = QLineEdit()
        self.material_input.setPlaceholderText("Material")
        form_layout.addRow("Material:", self.material_input)

        self.cantitate_input = QLineEdit()
        self.cantitate_input.setPlaceholderText("Cantitate")
        form_layout.addRow("Cantitate:", self.cantitate_input)

        # Add Form Layout to Main Layout
        layout.addLayout(form_layout)

        # Add Button
        add_button = QPushButton("Add Stup")
        add_button.clicked.connect(self.add_stup)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_stup(self):
        """
            Send a POST request to add a new stup.
        """
        # Get input
        tip = self.tip_input.text()
        numar_rame = self.numar_rame_input.text()
        dimensiuni = self.dimensiuni_input.text()
        material = self.material_input.text()
        cantitate = self.cantitate_input.text()

        # Check fields
        if not tip or not numar_rame or not dimensiuni or not material or not cantitate:
            QMessageBox.critical(self, "Input Error", "Toate câmpurile sunt obligatorii!")
            return

        # Data
        data = {
            "tip": tip,
            "numar_rame": numar_rame,
            "dimensiuni": dimensiuni,
            "material": material,
            "cantitate": cantitate
        }

        response = requests.post(f"{BASE_URL}/stup", json=data)

        if response.status_code == 201:
            QMessageBox.information(self, "Success", "Tip de stup adaugat cu succes!")
        else:
            QMessageBox.critical(
                self, "Error", f"Failed: {response.json().get('error', 'Unknown error')}"
            )