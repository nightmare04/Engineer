from PyQt6.QtCore import pyqtSignal

from custom_widgets.tables import *
from windows.adds import *


class ListAll(QDialog):
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


class UnitList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список подразделений")
        self.table = AllTableView(["", "Подразделения"], Unit)
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

    def edit(self, item):
        edit_item = Unit.get_by_id(item.siblingAtColumn(0).data())
        AddUnit(edit_item).exec()
        self.table.model.updateData()

    def add(self):
        AddUnit().exec()
        self.table.model.updateData()


class PlaneTypeList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список типов самолетов")
        self.table = AllTableView(["", "Тип"], PlaneType)
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

    def edit(self, item):
        edit_item = PlaneType.get_by_id(item.siblingAtColumn(0).data())
        AddPlaneType(edit_item).exec()
        self.table.model.updateData()

    def add(self):
        AddPlaneType().exec()
        self.table.model.updateData()


class OsobList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список особенностей самолетов")
        self.table = OsobPlaneTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

    def edit(self, item):
        edit_item = OsobPlane.get_by_id(item.siblingAtColumn(0).data())
        AddOsob(edit_item).exec()
        self.table.model.updateData()

    def add(self):
        AddOsob().exec()
        self.table.model.updateData()


class ZavodIzgList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список заводов изготовителей")
        self.table = AllTableView(["", "Завод"], ZavIzg)
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

    def edit(self, item):
        edit_item = ZavIzg.get_by_id(item.siblingAtColumn(0).data())
        AddZavodIzg(edit_item).exec()
        self.table.model.updateData()

    def add(self):
        AddZavodIzg().exec()
        self.table.model.updateData()


class ZavodRemList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список ремонтных заводов")
        self.table = AllTableView(["", "Завод"], RemZav)
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

    def edit(self, item):
        edit_item = RemZav.get_by_id(item.siblingAtColumn(0).data())
        AddZavodRem(edit_item).exec()
        self.table.model.updateData()

    def add(self):
        AddZavodRem().exec()
        self.table.model.updateData()


class SpecList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Специальности")
        self.table = AllTableView(["", "Специальность"], Spec)
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

    def edit(self, item):
        edit_item = Spec.get_by_id(item.siblingAtColumn(0).data())
        AddSpec(edit_item).exec()
        self.table.model.updateData()

    def add(self):
        AddSpec().exec()
        self.table.model.updateData()


class RemTypeList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список типов ремонта")
        self.table = RemTypeTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

    def edit(self, item):
        edit_item = RemType.get_by_id(item.siblingAtColumn(0).data())
        AddTypeRem(edit_item).exec()
        self.table.model.updateData()

    def add(self):
        AddTypeRem().exec()
        self.table.model.updateData()


class PlaneSystemList(ListAll):
    send_object = pyqtSignal(PlaneSystem)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список систем самолета")
        self.table = PlaneSystemTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

    def edit(self, item):
        edit_item = PlaneSystem.get_by_id(item.siblingAtColumn(0).data())
        edit_system = AddSystem()
        edit_system.update_signal.connect(self.update_table)
        self.send_object.connect(edit_system.edit)
        self.send_object.emit(edit_item)
        edit_system.exec()

    @pyqtSlot()
    def update_table(self):
        self.table.model.updateData()

    def add(self):
        add_system = AddSystem()
        add_system.update_signal.connect(self.update_table)
        add_system.exec()


class PlaneList(ListAll):
    send_object = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список самолетов")
        self.table = PlaneTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

    def edit(self, item):
        edit_window = AddPlane()
        self.send_object.connect(edit_window.edit_plane)
        edit_item_id = item.siblingAtColumn(0).data()
        self.send_object.emit(edit_item_id)
        edit_window.exec()
        self.table.model.updateData()

    def add(self):
        AddPlane().exec()
        self.table.model.updateData()