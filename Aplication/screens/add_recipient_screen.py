import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QMessageBox
import requests

BASE_URL = "http://localhost:5000" 

class AddRecipientScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Form Fields
        self.nume_recipient_input = QLineEdit()
        self.nume_recipient_input.setPlaceholderText("Nume Recipient")
        form_layout.addRow("Nume Recipient:", self.nume_recipient_input)

        self.numar_unitati_input = QLineEdit()
        self.numar_unitati_input.setPlaceholderText("Numar Unitati")
        form_layout.addRow("Numar Unitati:", self.numar_unitati_input)

        self.cantitate_input = QLineEdit()
        self.cantitate_input.setPlaceholderText("Cantitate")
        form_layout.addRow("Cantitate:", self.cantitate_input)

        self.unitate_cantitate_input = QLineEdit()
        self.unitate_cantitate_input.setPlaceholderText("Unitate Cantitate")
        form_layout.addRow("Unitate Cantitate:", self.unitate_cantitate_input)

        # Add Form Layout to Main Layout
        layout.addLayout(form_layout)

        # Button
        add_button = QPushButton("Add Recipient")
        add_button.clicked.connect(self.add_recipient)
        layout.addWidget(add_button)

        # Set layout to the window
        self.setLayout(layout)

    def add_recipient(self):
        """
            Send a POST request to add a new recipient.
        """
        nume_recipient = self.nume_recipient_input.text()
        numar_unitati = self.numar_unitati_input.text()
        cantitate = self.cantitate_input.text()
        unitate_cantitate = self.unitate_cantitate_input.text()

        # Check fields
        if not nume_recipient or not numar_unitati or not cantitate or not unitate_cantitate:
            QMessageBox.critical(self, "Error", f"Failed: {response.json().get('error', 'Unknown error')}")
            return

        # Data
        data = {
            "nume_recipient": nume_recipient,
            "numar_unitati": numar_unitati,
            "cantitate": cantitate,
            "unitate_cantitate": unitate_cantitate
        }

        # Sending POST request to the backend
        response = requests.post(f"{BASE_URL}/recipient", json=data)

        # Check if the response status code indicates success
        if response.status_code == 201:
            QMessageBox.information(self, "Success", "Recipient adaugat cu succes!")
        else:
            QMessageBox.critical(
            self, "Error", f"Failed to add Recipient: {response.json().get('error', 'Unknown error')}"
        )