from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QFormLayout, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt
from datetime import date
import requests

BASE_URL = "http://localhost:5000"

class AddInterventieScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Form Fields
        self.id_apicultor_input = QLineEdit()
        self.id_apicultor_input.setPlaceholderText("ID Apicultor")
        form_layout.addRow("ID Apicultor:", self.id_apicultor_input)

        self.id_familie_input = QLineEdit()
        self.id_familie_input.setPlaceholderText("ID Familie")
        form_layout.addRow("ID Familie:", self.id_familie_input)

        self.data_interventie_label = QLabel(f"Data Interventiei: {date.today().isoformat()}")
        form_layout.addRow(self.data_interventie_label)

        # Checkbox pentru alegerea operatiunilor
        self.tratament_checkbox = QCheckBox("Tratament")
        self.roire_checkbox = QCheckBox("Roire")
        self.schimbare_regina_checkbox = QCheckBox("Schimbare Regina")
        self.administrare_hrana_checkbox = QCheckBox("Administrare Hrana")
        self.extras_rame_checkbox = QCheckBox("Extras Rame")

        form_layout.addRow(self.tratament_checkbox)
        form_layout.addRow(self.roire_checkbox)
        form_layout.addRow(self.schimbare_regina_checkbox)
        form_layout.addRow(self.administrare_hrana_checkbox)
        form_layout.addRow(self.extras_rame_checkbox)

        # Câmpul de Observații
        self.observatii_input = QLineEdit()
        self.observatii_input.setPlaceholderText("Observatii")
        form_layout.addRow("Observații:", self.observatii_input)

        # Detalii (care se va completa pe baza checkbox-urilor selectate)
        self.detalii_input = QLineEdit()
        self.detalii_input.setPlaceholderText("Detalii operatie")
        form_layout.addRow("Detalii:", self.detalii_input)

        # Adăugăm toate câmpurile pentru operatiuni
        self.tratament_fields = self.create_tratament_fields()
        self.roire_fields = self.create_roire_fields()
        self.schimbare_regina_fields = self.create_schimbare_regina_fields()
        self.administrare_hrana_fields = self.create_administrare_hrana_fields()
        self.extras_rame_fields = self.create_extras_rame_fields()

        form_layout.addRow(self.tratament_fields)
        form_layout.addRow(self.roire_fields)
        form_layout.addRow(self.schimbare_regina_fields)
        form_layout.addRow(self.administrare_hrana_fields)
        form_layout.addRow(self.extras_rame_fields)

        # Add Form Layout to Main Layout
        layout.addLayout(form_layout)

        # Button pentru trimitere
        add_button = QPushButton("Adauga Interventie")
        add_button.clicked.connect(self.add_interventie)
        layout.addWidget(add_button)

        self.setLayout(layout)

        # Connect checkbox changes to update_fields
        self.tratament_checkbox.toggled.connect(self.update_fields)
        self.roire_checkbox.toggled.connect(self.update_fields)
        self.schimbare_regina_checkbox.toggled.connect(self.update_fields)
        self.administrare_hrana_checkbox.toggled.connect(self.update_fields)
        self.extras_rame_checkbox.toggled.connect(self.update_fields)

        # Setăm starea inițială
        self.update_fields()

    def create_tratament_fields(self):
        """
            Returnează câmpurile pentru tratament
        """
        layout = QFormLayout()
        self.tip_tratament_input = QLineEdit()
        self.tip_tratament_input.setPlaceholderText("Tip Tratament")
        layout.addRow("Tip Tratament:", self.tip_tratament_input)

        self.dozaj_input = QLineEdit()
        self.dozaj_input.setPlaceholderText("Doza Tratament")
        layout.addRow("Doza Tratament:", self.dozaj_input)

        return layout

    def create_roire_fields(self):
        """
            Returnează câmpurile pentru roire
        """
        layout = QFormLayout()
        self.provenienta_regina_input = QLineEdit()
        self.provenienta_regina_input.setPlaceholderText("Provenienta Regina")
        layout.addRow("Provenienta Regina:", self.provenienta_regina_input)

        self.tip_stup_input = QLineEdit()
        self.tip_stup_input.setPlaceholderText("Tip Stup")
        layout.addRow("Tip Stup:", self.tip_stup_input)

        return layout

    def create_schimbare_regina_fields(self):
        """
            Returnează câmpurile pentru schimbare regina
        """
        layout = QFormLayout()
        self.id_regina_input = QLineEdit()
        self.id_regina_input.setPlaceholderText("ID Regina")
        layout.addRow("ID Regina:", self.id_regina_input)

        return layout

    def create_administrare_hrana_fields(self):
        """
            Returnează câmpurile pentru administrare hrana
        """
        layout = QFormLayout()
        self.tip_hrana_input = QLineEdit()
        self.tip_hrana_input.setPlaceholderText("Tip Hrana")
        layout.addRow("Tip Hrana:", self.tip_hrana_input)

        self.cantitate_hrana_input = QLineEdit()
        self.cantitate_hrana_input.setPlaceholderText("Cantitate Hrana")
        layout.addRow("Cantitate Hrana:", self.cantitate_hrana_input)

        self.motiv_administrare_input = QLineEdit()
        self.motiv_administrare_input.setPlaceholderText("Motiv Administrare")
        layout.addRow("Motiv Administrare:", self.motiv_administrare_input)

        return layout

    def create_extras_rame_fields(self):
        """
            Returnează câmpurile pentru extras rame
        """
        layout = QFormLayout()
        self.numar_rame_extrase_input = QLineEdit()
        self.numar_rame_extrase_input.setPlaceholderText("Numar Rame Extrase")
        layout.addRow("Numar Rame Extrase:", self.numar_rame_extrase_input)

        self.cantitate_miere_input = QLineEdit()
        self.cantitate_miere_input.setPlaceholderText("Cantitate Miere")
        layout.addRow("Cantitate Miere:", self.cantitate_miere_input)

        self.observatii_rame_input = QLineEdit()
        self.observatii_rame_input.setPlaceholderText("Observații")
        layout.addRow("Observații:", self.observatii_rame_input)

        return layout

    def set_fields_disabled(self, checkbox, fields):
        """
            Setează câmpurile ca fiind dezactivate (gri) dacă checkbox-ul nu este selectat
        """
        state = Qt.Unchecked if not checkbox.isChecked() else Qt.Checked
        for field in fields:
            field.setEnabled(state == Qt.Checked)
            if state == Qt.Unchecked:
                field.setStyleSheet("background-color: lightgray; color: gray;")
            else:
                field.setStyleSheet("")

    def update_fields(self):
        """
            Actualizează câmpurile pe baza checkbox-urilor selectate
        """
        # Adăugăm operatiunile selectate în câmpul detalii
        detalii_text = []
        if self.tratament_checkbox.isChecked():
            detalii_text.append("Tratament")
        if self.roire_checkbox.isChecked():
            detalii_text.append("Roire")
        if self.schimbare_regina_checkbox.isChecked():
            detalii_text.append("Schimbare Regina")
        if self.administrare_hrana_checkbox.isChecked():
            detalii_text.append("Administrare Hrana")
        if self.extras_rame_checkbox.isChecked():
            detalii_text.append("Extras Rame")
        
        # Actualizăm câmpul "Detalii"
        self.detalii_input.setText(", ".join(detalii_text))

        # Actualizăm câmpurile pentru fiecare operatiune
        self.set_fields_disabled(self.tratament_checkbox, [self.tip_tratament_input, self.dozaj_input])
        self.set_fields_disabled(self.roire_checkbox, [self.provenienta_regina_input, self.tip_stup_input])
        self.set_fields_disabled(self.schimbare_regina_checkbox, [self.id_regina_input])
        self.set_fields_disabled(self.administrare_hrana_checkbox, [self.tip_hrana_input, self.cantitate_hrana_input, self.motiv_administrare_input])
        self.set_fields_disabled(self.extras_rame_checkbox, [self.numar_rame_extrase_input, self.cantitate_miere_input, self.observatii_rame_input])

    def add_interventie(self):
        """
            Send a POST request to add a new intervention.
        """        
        id_apicultor = self.id_apicultor_input.text()
        id_familie = self.id_familie_input.text()
        detalii = self.detalii_input.text()
        observatii = self.observatii_input.text()

        # Data
        data = {
            "id_apicultor": id_apicultor,
            "id_familie": id_familie,
            "detalii": detalii,
            "observatii": observatii
        }

        # Get the Data only from the fields asociated with the check checkboxes
        if self.tratament_checkbox.isChecked():
            data["tip_tratament"] = self.tip_tratament_input.text()
            data["doza"] = self.dozaj_input.text()

        if self.roire_checkbox.isChecked():
            data["provenienta_regina"] = self.provenienta_regina_input.text()
            data["tip_stup"] = self.tip_stup_input.text()

        if self.schimbare_regina_checkbox.isChecked():
            data["id_regina"] = self.id_regina_input.text()

        if self.administrare_hrana_checkbox.isChecked():
            data["tip_hrana"] = self.tip_hrana_input.text()
            data["cantitate_hrana"] = self.cantitate_hrana_input.text()
            data["motiv_administrare"] = self.motiv_administrare_input.text()

        if self.extras_rame_checkbox.isChecked():
            data["numar_rame_extrase"] = self.numar_rame_extrase_input.text()
            data["cantitate_miere"] = self.cantitate_miere_input.text()
            data["observatii_extras_rame"] = self.observatii_rame_input.text()

        response = requests.post(f"{BASE_URL}/add_interventie", json=data)
        if response.status_code == 201:
            QMessageBox.information(self, "Success", "Intervenția a fost adăugată cu succes!")
        else:
            QMessageBox.critical(self, "Error", f"Eșec la adăugarea intervenției: {response.json().get('error', 'Error necunoscut')}")