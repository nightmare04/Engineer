from PyQt6.QtCore import pyqtSignal

from custom_widgets.tables import *
from windows.adds import *


class ListAll(QDialog):
    send = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(500, 500)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.btnLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.btnLayout)
        self.btnOk = QPushButton("Ок")
        self.btnOk.clicked.connect(self.accept)
        self.btnAdd = QPushButton("Добавить")
        self.btnAdd.clicked.connect(self.add)
        self.btnLayout.addWidget(self.btnOk)
        self.btnLayout.addWidget(self.btnAdd)

    def edit(self, item):
        edit_item_id = item.siblingAtColumn(0).data()
        self.send.emit(str(edit_item_id))
        self.edit_window.exec()

    def add(self):
        self.edit_window.exec()

    @pyqtSlot()
    def update_table(self):
        self.table.model.updateData()


class UnitList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список подразделений")

        self.table = AllTableView(["", "Подразделения"], Unit)
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

        self.edit_window = AddUnit()
        self.edit_window.update_signal.connect(self.update_table)
        self.send.connect(self.edit_window.edit)


class PlaneTypeList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список типов самолетов")

        self.table = AllTableView(["", "Тип"], PlaneType)
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

        self.edit_window = AddPlaneType()
        self.edit_window.update_signal.connect(self.update_table)
        self.send.connect(self.edit_window.edit)


class OsobList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список особенностей самолетов")

        self.table = OsobPlaneTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

        self.edit_window = AddOsob()
        self.edit_window.update_signal.connect(self.update_table)
        self.send.connect(self.edit_window.edit)


class ZavodIzgList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список заводов изготовителей")
        self.table = AllTableView(["", "Завод"], ZavIzg)
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

        self.edit_window = AddZavodIzg()
        self.edit_window.update_signal.connect(self.update_table)
        self.send.connect(self.edit_window.edit)


class ZavodRemList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список ремонтных заводов")
        self.table = AllTableView(["", "Завод"], RemZav)
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

        self.edit_window = AddZavodRem()
        self.edit_window.update_signal.connect(self.update_table)
        self.send.connect(self.edit_window.edit)


class SpecList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Специальности")
        self.table = AllTableView(["", "Специальность"], Spec)
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

        self.edit_window = AddSpec()
        self.edit_window.update_signal.connect(self.update_table)
        self.send.connect(self.edit_window.edit)


class RemTypeList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список типов ремонта")
        self.table = RemTypeTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

        self.edit_window = AddTypeRem()
        self.edit_window.update_signal.connect(self.update_table)
        self.send.connect(self.edit_window.edit)


class PlaneList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список самолетов")
        self.table = PlaneTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

        self.edit_window = AddPlane()
        self.edit_window.update_signal.connect(self.update_table)
        self.send.connect(self.edit_window.edit)


class PlaneSystemList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список систем самолета")
        self.table = PlaneSystemTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

        self.edit_window = AddSystem()
        self.edit_window.update_signal.connect(self.update_table)
        self.send.connect(self.edit_window.edit)

        self.filter_layout = QFormLayout()
        self.mainLayout.insertLayout(1, self.filter_layout)
        self.type_filter = TypePlaneComboBox(PlaneType.select().where(PlaneType.not_delete == True))
        self.spec_filter = SpecComboBox(Spec.select().where(Spec.not_delete == True))
        self.filter_layout.addRow("Выберите тип самолета", self.type_filter)
        self.filter_layout.addRow("Выберите специальность", self.spec_filter)

        self.type_filter.currentTextChanged.connect(self.table.proxy_model.setTypeFilter)
        self.spec_filter.currentTextChanged.connect(self.table.proxy_model.setSpecFilter)


class AgregateStateList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список состояний блока/агрегата")
        self.table = AgregateStateTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

        self.edit_window = AddAgregateState()
        self.edit_window.update_signal.connect(self.update_table)
        self.send.connect(self.edit_window.edit)


class AgregateNameList(ListAll):
    pass

