from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QComboBox, QTableView, QMessageBox, QLabel
)
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
import requests

BASE_URL = "http://localhost:5000"

class DynamicTableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self.data = data
        self.headers = headers

    def rowCount(self, parent=QModelIndex()):
        return len(self.data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = self.data[index.row()]
            column = self.headers[index.column()]
            return row.get(column, "")

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return None

class DataViewer(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        layout = QVBoxLayout()

        # Dropdown for selecting data source
        self.dropdown = QComboBox()
        self.dropdown.addItem("Selecteaza ce date vrei sa vizualizezi", "")
        self.dropdown.addItem("Apicultori", "apicultori")
        self.dropdown.addItem("Recipient", "recipient")
        self.dropdown.addItem("Miere", "miere")
        self.dropdown.addItem("Produse", "produs")
        self.dropdown.addItem("Intervenții", "get_interventii")
        self.dropdown.addItem("Familie de Albine", "get_data_fam_albine")
        layout.addWidget(QLabel("Select a data source:"))
        layout.addWidget(self.dropdown)

        # Manual mapping of dropdown item names to backend endpoints
        self.endpoint_mapping = {
            "Apicultori": "apicultori",
            "Recipient": "recipient",
            "Miere": "miere",
            "Produse": "produs",
            "Intervenții": "get_interventii",
            "Familie de Albine": "get_data_fam_albine",
        }

        # Connect dropdown selection change to handler
        self.dropdown.currentTextChanged.connect(self.on_selection_changed)

        # Table view to display fetched data
        self.table_view = QTableView()
        layout.addWidget(self.table_view)

        self.setLayout(layout)
        self.setWindowTitle("Dynamic Data Viewer")
        self.setGeometry(100, 100, 800, 600)

    def on_selection_changed(self):
        """
            Fetch and display data for the selected item.
        """
        selected_item = self.dropdown.currentText()
        endpoint = self.endpoint_mapping.get(selected_item)

        if endpoint:
            self.fetch_and_display_data(endpoint)

    def fetch_and_display_data(self, endpoint):
        """
            Fetch data from the backend and display it in the table.
        """
        response = requests.get(f"{BASE_URL}/{endpoint}")

        if response.status_code == 201:
            data = response.json()

            if isinstance(data, list) and len(data) > 0:
                headers = list(data[0].keys())
                model = DynamicTableModel(data, headers)
                self.table_view.setModel(model)
                
            else:
                QMessageBox.information(self, "No Data", "Nu există date disponibile pentru această sursă.")
        else:
            QMessageBox.critical(self, "Error", f"Nu s-au putut încărca datele.\n{response.text}")
