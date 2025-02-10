import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout,
    QListWidget, QStackedWidget, QWidget, QPushButton
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

# All the screen classes
from screens.add_apicultor_screen import AddApicultorScreen
from screens.add_regina_screen import AddReginaScreen
from screens.add_stup_screen import AddStupScreen
from screens.add_recipient_screen import AddRecipientScreen
from screens.add_familie_de_albine_screen import AddFamilieDeAlbineScreen
from screens.pack_honey_screen import PackHoneyScreen
from screens.add_interventie_screen import AddInterventieScreen
from screens.add_vanzare_screen import AddVanzareScreen
from screens.vanzari_produse_screen import VanzariProduseScreen
from screens.apicultori_experienta_maestru import ApicultoriTreemapScreen
from screens.StupiBarPlotScreen import StupiBarChartScreen
from screens.data_viewer import DataViewer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicatie Apicultura")

        main_layout = QHBoxLayout()

        # Navigation Menu
        self.menu_list = QListWidget()
        self.menu_list.addItem("Adauga Apicultor")
        self.menu_list.addItem("Adauga Regina")
        self.menu_list.addItem("Adauga Stup")
        self.menu_list.addItem("Adauga Recipient Miere")
        self.menu_list.addItem("Adauga Familie de Albine")
        self.menu_list.addItem("Imbuteliaza Miere")
        self.menu_list.addItem("Adauga Interventie")
        self.menu_list.addItem("Vanzare")
        self.menu_list.addItem("Raport Vanzari")
        self.menu_list.addItem("Raport Apicultori") #
        self.menu_list.addItem("Raport Stupi") #
        self.menu_list.addItem("Vizualizare Date")
        self.menu_list.currentItemChanged.connect(self.change_screen)

        # Refresh button
        self.refresh_button = QPushButton()
        self.refresh_button.setIcon(QIcon.fromTheme("view-refresh"))  # Use a default theme icon
        self.refresh_button.setIconSize(QSize(24, 24))  # Set icon size
        self.refresh_button.clicked.connect(self.refresh_screen)

        # Left side layout (menu + refresh button)
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.refresh_button)
        left_layout.addWidget(self.menu_list)
        left_layout.addStretch()

        # Stacked Widget
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(AddApicultorScreen())
        self.stacked_widget.addWidget(AddReginaScreen())
        self.stacked_widget.addWidget(AddStupScreen())
        self.stacked_widget.addWidget(AddRecipientScreen())
        self.stacked_widget.addWidget(AddFamilieDeAlbineScreen())
        self.stacked_widget.addWidget(PackHoneyScreen())
        self.stacked_widget.addWidget(AddInterventieScreen())
        self.stacked_widget.addWidget(AddVanzareScreen())
        self.stacked_widget.addWidget(VanzariProduseScreen())
        self.stacked_widget.addWidget(ApicultoriTreemapScreen()) #
        self.stacked_widget.addWidget(StupiBarChartScreen()) #
        self.stacked_widget.addWidget(DataViewer())

        # Add layouts to the main layout
        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.stacked_widget)

        # Set the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def change_screen(self, current, previous):
        if current is None:
            return
        self.stacked_widget.setCurrentIndex(self.menu_list.row(current))

    def refresh_screen(self):
        """Refreshes the current screen"""
        current_index = self.stacked_widget.currentIndex()
        # Create a new instance of the current widget and replace it
        if current_index == 0:
            self.stacked_widget.insertWidget(current_index, AddApicultorScreen())
        elif current_index == 1:
            self.stacked_widget.insertWidget(current_index, AddReginaScreen())
        elif current_index == 2:
            self.stacked_widget.insertWidget(current_index, AddStupScreen())
        elif current_index == 3:
            self.stacked_widget.insertWidget(current_index, AddRecipientScreen())
        elif current_index == 4:
            self.stacked_widget.insertWidget(current_index, AddFamilieDeAlbineScreen())
        elif current_index == 5:
            self.stacked_widget.insertWidget(current_index, PackHoneyScreen())
        elif current_index == 6:
            self.stacked_widget.insertWidget(current_index, AddInterventieScreen())
        elif current_index == 7:
            self.stacked_widget.insertWidget(current_index, AddVanzareScreen())
        elif current_index == 8:
            self.stacked_widget.insertWidget(current_index, VanzariProduseScreen())
        elif current_index == 9:
            self.stacked_widget.insertWidget(current_index, ApicultoriTreemapScreen()) # 
        elif current_index == 10:
            self.stacked_widget.insertWidget(current_index, StupiBarChartScreen()) #
        elif current_index == 11:
            self.stacked_widget.insertWidget(current_index, DataViewer())
    
        self.stacked_widget.removeWidget(self.stacked_widget.widget(current_index))
        self.stacked_widget.setCurrentIndex(current_index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
