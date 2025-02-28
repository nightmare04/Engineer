from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy


class LeftDock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.btnLC = QPushButton("Листы контроля")
        self.mainLayout.addWidget(self.btnLC)

        self.btnIspr = QPushButton("Исправность")
        self.mainLayout.addWidget(self.btnIspr)

        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.mainLayout.addItem(spacer)
