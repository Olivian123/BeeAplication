from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QFormLayout, QMessageBox, QComboBox, QSpinBox
import requests

BASE_URL = "http://localhost:5000" 

class PackHoneyScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Dropdown for Honey Type (Miere)
        self.honey_dropdown = QComboBox()
        self.load_honey_data()
        form_layout.addRow("Honey:", self.honey_dropdown)

        # Dropdown for Recipient
        self.recipient_dropdown = QComboBox()
        self.load_recipient_data()
        form_layout.addRow("Recipient:", self.recipient_dropdown)

        self.max_age_input = QSpinBox()
        self.max_age_input.setRange(1, 100)
        self.max_age_input.setSuffix(" years")
        form_layout.addRow("Maximum Age:", self.max_age_input)

        self.num_units_input = QSpinBox()
        # Assuming reasonable limits
        self.num_units_input.setRange(1, 1000)  
        form_layout.addRow("Number of Units:", self.num_units_input)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Enter price")
        form_layout.addRow("Price:", self.price_input)

        layout.addLayout(form_layout)

        # Button
        pack_button = QPushButton("Pack Honey")
        pack_button.clicked.connect(self.pack_honey)
        layout.addWidget(pack_button)

        # Result Label
        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def load_honey_data(self):
        """
            Load honey data from the backend and populate dropdown.
        """
        response = requests.get(f"{BASE_URL}/miere")
        
        if response.status_code == 201:
            honey_list = response.json()

            # Display type and quantity in the dropdown
            for honey in honey_list:
                self.honey_dropdown.addItem(
                    f"{honey['id_miere']} - {honey['tip']} ({honey['cantitate']} kg)",
                    userData=honey
                )
        else:
            self.honey_dropdown.addItem("Error")

    def load_recipient_data(self):
        """
            Load recipient data from the backend and populate dropdown.
        """
        response = requests.get(f"{BASE_URL}/recipient")

        if response.status_code == 201:
            recipient_list = response.json()

            # Display name and number of units in the dropdown
            for recipient in recipient_list:
                self.recipient_dropdown.addItem(
                    f"{recipient['id_recipient']} - {recipient['nume_recipient']} "
                    f"({recipient['numar_unitati']} units, {recipient['cantitate']} L/unit)",
                    userData=recipient
                )
        else:
            self.recipient_dropdown.addItem("Error loading recipient data")

    def pack_honey(self):
        """
            Send a POST request to pack honey.
        """
        selected_honey = self.honey_dropdown.currentData()
        selected_recipient = self.recipient_dropdown.currentData()

        if not selected_honey or not selected_recipient:
            QMessageBox.warning(self, "Validation Error", "Selecteaza un recipient valid!")
            return

        tip_miere = selected_honey["tip"]
        vechime_maxima = self.max_age_input.value()
        nume_recipient = selected_recipient["nume_recipient"]
        numar_unitati = self.num_units_input.value()
        pret = self.price_input.text()

        # Validate input
        if not pret or not pret.replace('.', '', 1).isdigit():
            QMessageBox.warning(self, "Validation Error", "Adauga pret valid!")
            return

        data = {
            "tip_miere": tip_miere,
            "vechime_maxima": vechime_maxima,
            "nume_recipient": nume_recipient,
            "numar_unitati": numar_unitati,
            "pret": float(pret),
        }

        response = requests.post(f"{BASE_URL}/pack_honey", json=data)

        if response.status_code == 200:
            result = response.json()
            QMessageBox.information(
                self,
                "Success",
                f"Honey packed successfully!"
            )
        else:
            error = response.json().get("error", "Unknown error occurred.")
            QMessageBox.critical(self, "Error", f"Failed to pack honey: {error}")
