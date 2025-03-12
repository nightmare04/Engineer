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
        edit_window = self.edit_obj()
        edit_window.update_signal.connect(self.update_table)
        self.send.connect(edit_window.edit)
        edit_item_id = item.siblingAtColumn(0).data()
        self.send.emit(str(edit_item_id))
        edit_window.exec()

    def add(self):
        add_window = self.edit_obj()
        add_window.update_signal.connect(self.update_table)
        add_window.exec()

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
        self.edit_obj = AddUnit


class PlaneTypeList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список типов самолетов")

        self.table = AllTableView(["", "Тип"], PlaneType)
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

        self.edit_obj = AddPlaneType


class OsobList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список особенностей самолетов")

        self.table = OsobPlaneTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

        self.edit_obj = AddOsob


class ZavodIzgList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список заводов изготовителей")
        self.table = AllTableView(["", "Завод"], ZavIzg)
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)
        self.edit_obj = AddZavodIzg


class ZavodRemList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список ремонтных заводов")
        self.table = AllTableView(["", "Завод"], RemZav)
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

        self.edit_obj = AddZavodRem


class SpecList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Специальности")
        self.table = AllTableView(["", "Специальность"], Spec)
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)
        self.edit_obj = AddSpec


class RemTypeList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список типов ремонта")
        self.table = RemTypeTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)
        self.edit_obj = AddTypeRem


class PlaneList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список самолетов")
        self.resize(1100, 600)
        self.table = PlaneTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)
        self.edit_obj = AddPlane


class PlaneSystemList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список систем самолета")
        self.table = PlaneSystemTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)
        self.edit_obj = AddSystem

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
        self.edit_obj = AddAgregateState


class AgregateNameList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список наименований блоков")
        self.table = AgregateNameTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

        self.filterLayout = QFormLayout()
        self.plane_type_cb = TypePlaneComboBox(PlaneType.select().where(PlaneType.not_delete == True))
        self.spec_cb = SpecComboBox(Spec.select().where(Spec.not_delete == True))
        self.system_cb = SystemComboBox(PlaneSystem.select().where(PlaneSystem.not_delete == True))
        self.filterLayout.addRow("Выбери тип", self.plane_type_cb)
        self.filterLayout.addRow("Выбери специальность", self.spec_cb)
        self.filterLayout.addRow("Выбери систему", self.system_cb)
        self.mainLayout.insertLayout(1, self.filterLayout)

        self.plane_type_cb.currentTextChanged.connect(self.changeData)
        self.spec_cb.currentTextChanged.connect(self.changeData)

        self.plane_type_cb.currentTextChanged.connect(self.table.proxy_model.setTypeFilter)
        self.spec_cb.currentTextChanged.connect(self.table.proxy_model.setSpecFilter)
        self.system_cb.currentTextChanged.connect(self.table.proxy_model.setSystemFilter)

        self.edit_obj = AddAgregateName
        self.changeData()

    def changeData(self):
        self.system_cb.model.updateData(
            (PlaneSystem.select().where(PlaneSystem.specId == self.spec_cb.currentData(Qt.ItemDataRole.UserRole),
                                        PlaneSystem.typeId == self.plane_type_cb.currentData(
                                            Qt.ItemDataRole.UserRole))))
