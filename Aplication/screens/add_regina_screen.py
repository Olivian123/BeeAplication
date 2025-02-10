
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QFormLayout, QMessageBox
from datetime import date
import requests

BASE_URL = "http://localhost:5000" 

class AddReginaScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.tip_regina_input = QLineEdit()
        self.tip_regina_input.setPlaceholderText("Tip Regina")
        form_layout.addRow("Tip Regina:", self.tip_regina_input)

        self.data_imperechere_input = QLineEdit()
        self.data_imperechere_input.setPlaceholderText("Data Imperechere")
        form_layout.addRow("Data Imperechere:", self.data_imperechere_input)

        self.status_input = QLineEdit()
        self.status_input.setPlaceholderText("Status")
        form_layout.addRow("Status:", self.status_input)

        self.varsta_input = QLineEdit()
        self.varsta_input.setPlaceholderText("Varsta")
        form_layout.addRow("Varsta:", self.varsta_input)

        self.provenienta_input = QLineEdit()
        self.provenienta_input.setPlaceholderText("Provenienta")
        form_layout.addRow("Provenienta:", self.provenienta_input)

        # Label to display ID Regina When the operation is completed successfuly
        self.id_regina_label = QLabel("ID Regina: N/A")
        form_layout.addRow(self.id_regina_label)

        layout.addLayout(form_layout)

        # Add Button
        add_button = QPushButton("Add Regina")
        add_button.clicked.connect(self.add_regina)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_regina(self):
        """
            Send a POST request to add a new Regina.
        """
        tip_regina = self.tip_regina_input.text()
        data_imperechere = self.data_imperechere_input.text()
        status = self.status_input.text()
        varsta = self.varsta_input.text()
        provenienta = self.provenienta_input.text()

        # Check data
        if not all([tip_regina, data_imperechere, status, varsta, provenienta]):
            QMessageBox.critical(self, "Input Error", "Toate câmpurile sunt obligatorii!")
            return

        # Data
        data = {
            "tip_regina": tip_regina,
            "data_imperechere": data_imperechere,
            "status": status,
            "varsta": varsta,
            "provenienta": provenienta
        }

        # POST request
        response = requests.post(f"{BASE_URL}/regina", json=data)

        if response.status_code == 201:
            response_data = response.json()
            id_regina = response_data['id_regina']

            # Update the ID Regina label on the screen
            self.id_regina_label.setText(f"ID Regina: {id_regina}")
            QMessageBox.information(self, "Success", "Regina added successfully!")
        else:
            QMessageBox.critical(self, "Error", "Failed!")
