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
        self.table = AllTableView(["", "Завод"], VypZav)
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

    def edit(self, item):
        edit_item = VypZav.get_by_id(item.siblingAtColumn(0).data())
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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список систем самолета")
        self.table = PlaneSystemTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

    def edit(self, item):
        edit_item = PlaneSystem.get_by_id(item.siblingAtColumn(0).data())
        AddPlaneSystem(edit_item).exec()
        self.table.model.updateData()

    def add(self):
        AddPlaneSystem().exec()
        self.table.model.updateData()


class PlaneList(ListAll):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Список самолетов")
        self.table = PlaneTableView()
        self.mainLayout.insertWidget(0, self.table)
        self.table.doubleClicked.connect(self.edit)

    def edit(self, item):
        edit_item = PlaneSystem.get_by_id(item.siblingAtColumn(0).data())
        AddPlane(edit_item).exec()
        self.table.model.updateData()

    def add(self):
        AddPlane().exec()
        self.table.model.updateData()