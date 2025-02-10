from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QFormLayout, QMessageBox, QComboBox
import requests

BASE_URL = "http://localhost:5000"

class AddFamilieDeAlbineScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.id_regina_input = QLineEdit()
        self.id_regina_input.setPlaceholderText("ID Regina")
        form_layout.addRow("ID Regina:", self.id_regina_input)

        self.tip_stup_input = QComboBox()
        self.load_stupi()
        form_layout.addRow("Tip Stup:", self.tip_stup_input)

        # Add Form Layout to Main Layout
        layout.addLayout(form_layout)

        # Button
        add_button = QPushButton("Add Familie de Albine")
        add_button.clicked.connect(self.add_familie_de_albine)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def load_stupi(self):
        """
            Load available bee box types into the dropdown.
        """
        response = requests.get(f"{BASE_URL}/stupi")

        if response.status_code == 200:
            stup_list = response.json()
            for stup in stup_list:
                self.tip_stup_input.addItem(stup['tip'] + " " + str(stup['numar_rame'])  + " Cantitate : " + str(stup['cantitate']) )
        else:
            QMessageBox.critical(self, "Error", "Failed to load all types.")


    def get_id_stup(self, tip_stup):
        """
            Retrieve id_stup for the selected tip.
        """
        response = requests.get(f"{BASE_URL}/stup", json={"tip": tip_stup})

        if response.status_code == 201:
            stup_data = response.json()
            
            return stup_data[0]['id_stup']      
        else:
            QMessageBox.critical(self, "Error", f"Failed: {response.json().get('error', 'Unknown error')}")
            
            return None
        

    def add_familie_de_albine(self):
        """
            Send a POST request to add a new Familie de Albine.
        """
        id_regina = self.id_regina_input.text()
        tip_stup = self.tip_stup_input.currentText().split()[0]

        # Check data
        if not id_regina:
            QMessageBox.critical(self, "Input Error", "Nici o regina gasita!")
            return

        id_stup = self.get_id_stup(tip_stup)

        if not id_stup:
            QMessageBox.critical(self, "Input Error", "Nici o cutie gasita!")
            return

        # Data
        data = {
            "id_regina": id_regina,
            "id_stup": id_stup
        }

        response = requests.post(f"{BASE_URL}/familii_de_albine", json=data)

        # Check if the response status code indicates success
        if response.status_code == 201:
            QMessageBox.information(self, "Success", "Familie de Albine adaugata cu succes!")
        else:
            QMessageBox.critical(self, "Error", f"Failed: {response.json().get('error', 'Unknown error')}")