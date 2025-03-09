from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QFormLayout, QLineEdit, QDateEdit

from custom_widgets.buttons import OsobBtn
from custom_widgets.combobox import (TypePlaneComboBox, UnitComboBox, RemZavComboBox, VypZavComboBox, RemTypeComboBox,
                                     SpecComboBox)
from custom_widgets.groupboxs import OsobGroupBox
from database.models import PlaneType, Plane, Unit, Spec, RemType, RemZav, VypZav, OsobPlane, PlaneSystem


class Adds(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(500, 500)
        self.mainlayout = QVBoxLayout(self)
        self.setLayout(self.mainlayout)

        self.form = QFormLayout()
        self.btnlayout = QHBoxLayout()

        self.btn_ok = QPushButton("Ок")
        self.btn_cancel = QPushButton("Отменить")
        self.btnlayout.addWidget(self.btn_ok)
        self.btnlayout.addWidget(self.btn_cancel)

        self.mainlayout.addLayout(self.form)
        self.mainlayout.addLayout(self.btnlayout)

        self.btn_ok.clicked.connect(self.add)
        self.btn_cancel.clicked.connect(self.reject)


class AddUnit(Adds):
    def __init__(self, unit: Unit = None, parent=None):
        super().__init__(parent)
        self.unit = unit
        self.setWindowTitle("Добавить подразделение")
        self.unit_name = QLineEdit()
        self.form.addRow("Подразделение", self.unit_name)
        if unit is not None:
            self.setWindowTitle("Изменить подразделение")
            self.btn_del = QPushButton("Удалить")
            self.btn_del.clicked.connect(self.delete)
            self.btnlayout.addWidget(self.btn_del)

            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.save)
            self.load()

    def add(self):
        unit = Unit()
        unit.name = self.unit_name.text()
        unit.save()
        self.clear()

    def save(self):
        self.unit.name = self.unit_name.text()
        self.unit.save()
        self.accept()

    def clear(self):
        self.unit_name.setText("")

    def load(self):
        self.unit_name.setText(self.unit.name)

    def delete(self):
        self.unit.not_delete = False
        self.unit.save()
        self.accept()


class AddPlaneType(Adds):
    def __init__(self, plane_type: PlaneType = None, parent=None):
        super().__init__(parent)
        self.plane_type = plane_type
        self.setWindowTitle("Добавить тип самолета")
        self.type_name = QLineEdit()
        self.form.addRow("Тип", self.type_name)
        if plane_type is not None:
            self.setWindowTitle("Изменить тип самолета")
            self.btn_del = QPushButton("Удалить")
            self.btn_del.clicked.connect(self.delete)
            self.btnlayout.addWidget(self.btn_del)

            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.save)
            self.load()

    def add(self):
        plane_type = PlaneType()
        plane_type.name = self.type_name.text()
        plane_type.save()
        self.clear()

    def save(self):
        self.plane_type.name = self.type_name.text()
        self.plane_type.save()
        self.accept()

    def clear(self):
        self.type_name.setText("")

    def load(self):
        self.type_name.setText(self.plane_type.name)

    def delete(self):
        self.plane_type.not_delete = False
        self.plane_type.save()
        self.accept()


class AddPlane(Adds):
    def __init__(self, basemodel, plane: Plane = None, parent=None):
        super().__init__(parent)
        self.instance = basemodel
        self.plane = plane
        self.setWindowTitle("Добавить самолет")
        self.planeType_combobox = TypePlaneComboBox(PlaneType.select().where(PlaneType.not_delete == True))
        self.unit_combobox = UnitComboBox(Unit.select().where(Unit.not_delete == True))
        self.bortNum = QLineEdit()
        self.zavNum = QLineEdit()
        self.dateVyp = QDateEdit()
        self.vypZav = VypZavComboBox(VypZav.select())
        self.dateRem = QDateEdit()
        self.remZav = RemZavComboBox(RemZav.select())
        self.remType = RemTypeComboBox(RemType.select())
        self.osobPlane = OsobGroupBox()

        self.form.addRow("Тип самолета", self.planeType_combobox)
        self.form.addRow("Подразделение", self.unit_combobox)
        self.form.addRow("Бортовой номер", self.bortNum)
        self.form.addRow("Заводской номер", self.zavNum)
        self.form.addRow("Дата выпуска", self.dateVyp)
        self.form.addRow("Завод изготовитель", self.vypZav)
        self.form.addRow("Дата ремонта", self.dateRem)
        self.form.addRow("АРЗ", self.remZav)
        self.form.addRow("Вид ремонта", self.remType)
        self.form.addRow("Особенности самолета", self.osobPlane)

        if self.plane is not None:
            self.setWindowTitle("Изменить самолет")
            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.update_plane)
            self.load()

            self.btn_del = QPushButton("Удалить")
            self.btnlayout.addWidget(self.btn_del)
            self.btn_del.clicked.connect(self.delete)

    def add(self):
        plane = Plane()
        plane.planeType = self.planeType_combobox.currentData()
        plane.unit = self.unit_combobox.currentData()
        plane.name = self.bortNum.text()
        plane.zavNum = self.zavNum.text()
        plane.dateVyp = self.dateVyp.date().toPyDate()
        plane.vypZav = self.vypZav.currentData()
        plane.dateRem = self.dateRem.date().toPyDate()
        plane.remZav = self.remZav.currentData()
        plane.remType = self.remType.currentData()
        plane.osobPlane = self.osob_dump()
        plane.save()
        self.clean()

    def osob_dump(self):
        res = []
        for osob_btn in self.findChildren(OsobBtn):
            if osob_btn.isChecked():
                res.append(osob_btn.osob_plane.id)
        return res

    def clean(self):
        self.bortNum.setText("")
        self.zavNum.setText("")
        self.dateVyp.clear()
        self.dateRem.clear()

    def load(self):
        self.bortNum.setText(self.plane.name)
        self.zavNum.setText(self.plane.zavNum)
        self.planeType_combobox.setCurrentIndex(self.planeType_combobox.findData(str(self.plane.planeType)))
        self.unit_combobox.setCurrentIndex(self.unit_combobox.findData(str(self.plane.unit)))
        self.bortNum.setText(self.plane.name)
        self.zavNum.setText(self.plane.zavNum)
        self.dateVyp.setDate(self.plane.dateVyp)
        self.vypZav.setCurrentIndex(self.vypZav.findData(str(self.plane.vypZav)))
        self.dateRem.setDate(self.plane.dateRem)
        self.remZav.setCurrentIndex(self.remZav.findData(str(self.plane.remZav)))
        self.remType.setCurrentIndex(self.remType.findData(str(self.plane.remType)))
        for osob_btn in self.osobPlane.findChildren(OsobBtn):
            for osob in self.plane.osobPlane:
                if osob_btn.osob_plane.id == osob:
                    osob_btn.setChecked(True)
        self.btn_ok.setText("Сохранить")
        self.btn_ok.clicked.disconnect()
        self.btn_ok.clicked.connect(self.update_plane)

    def update_plane(self):
        self.plane.planeType = self.planeType_combobox.currentData()
        self.plane.unit = self.unit_combobox.currentData(role=Qt.ItemDataRole.UserRole)
        self.plane.name = self.bortNum.text()
        self.plane.zavNum = self.zavNum.text()
        self.plane.dateVyp = self.dateVyp.date().toPyDate()
        self.plane.vypZav = self.vypZav.currentData(role=Qt.ItemDataRole.UserRole)
        self.plane.dateRem = self.dateRem.date().toPyDate()
        self.plane.remZav = self.remZav.currentData(role=Qt.ItemDataRole.UserRole)
        self.plane.remType = self.remType.currentData(role=Qt.ItemDataRole.UserRole)
        self.plane.osobPlane = self.osob_dump()
        self.plane.save()
        self.accept()

    def delete(self):
        self.plane.not_delete = False
        self.plane.save()
        self.accept()


class AddOsob(Adds):
    def __init__(self,  osob: OsobPlane = None, parent=None):
        super().__init__(parent)
        self.osob = osob
        self.setWindowTitle("Добавить особенность")
        self.osob_edit = QLineEdit()
        self.plane_type = TypePlaneComboBox(PlaneType.select().where(PlaneType.not_delete == True))
        self.form.addRow("Тип самолета", self.plane_type)
        self.form.addRow("&Наименование", self.osob_edit)
        if self.osob is not None:
            self.setWindowTitle("Изменить")
            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.save)
            self.load()
            self.btn_del = QPushButton("Удалить")
            self.btnlayout.addWidget(self.btn_del)
            self.btn_del.clicked.connect(self.delete)

    def add(self):
        osob = OsobPlane()
        osob.name = self.osob_edit.text()
        osob.planeType = self.plane_type.currentData(Qt.ItemDataRole.UserRole)
        osob.save()
        self.accept()

    def load(self):
        self.osob_edit.setText(self.osob.name)
        self.plane_type.setCurrentIndex(self.plane_type.findData(self.osob.planeType.id))

    def save(self):
        self.osob.name = self.osob_edit.text()
        self.osob.planeType = self.plane_type.currentData(Qt.ItemDataRole.UserRole)
        self.osob.save()
        self.accept()

    def delete(self):
        self.osob.not_delete = False
        self.osob.save()
        self.accept()


class AddSystem(Adds):
    def __init__(self, basemodel, system: PlaneSystem = None, parent=None):
        super().__init__(parent)
        self.instance = basemodel
        self.system = system
        self.setWindowTitle("Добавить систему самолета")
        self.system_edit = QLineEdit()
        self.spec = SpecComboBox(Spec.select().where(Spec.not_delete == True))
        self.plane_type = TypePlaneComboBox(PlaneType.select().where(PlaneType.not_delete == True))
        self.form.addRow("Тип самолета", self.plane_type)
        self.form.addRow("Специальность", self.spec)
        self.form.addRow("Название системы", self.system_edit)
        if self.system is not None:
            self.setWindowTitle("Изменить")
            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.save)
            self.load()

            self.btn_del = QPushButton("Удалить")
            self.btnlayout.addWidget(self.btn_del)
            self.btn_del.clicked.connect(self.delete)

    def add(self):
        system = PlaneSystem()
        system.name = self.system_edit.text()
        system.typeId = self.planeType.currentData(role=Qt.ItemDataRole.UserRole)
        system.specId = self.spec.currentData(role=Qt.ItemDataRole.UserRole)
        system.save()
        self.accept()

    def load(self):
        self.system_edit.setText(self.system.name)
        self.spec.setCurrentIndex(self.spec.findData(self.system.specId, role=Qt.ItemDataRole.UserRole))
        self.plane_type.setCurrentIndex(self.plane_type.findData(self.system.typeId, role=Qt.ItemDataRole.UserRole))

    def save(self):
        self.system.name = self.system_edit.text()
        self.system.specId = self.spec.currentData(role=Qt.ItemDataRole.UserRole)
        self.system.typeId = self.plane_type.currentData(role=Qt.ItemDataRole.UserRole)
        self.system.save()
        self.accept()

    def delete(self):
        self.system.not_delete = False
        self.system.save()
        self.accept()


class AddZavodIzg(Adds):
    def __init__(self, zavod_izg: VypZav = None, parent=None):
        super().__init__(parent)
        self.zavod_izg = zavod_izg
        self.setWindowTitle("Добавить завод изготовитель")
        self.zavod_izg_edit = QLineEdit()
        self.form.addRow("Завод изготовитель", self.zavod_izg_edit)
        if self.zavod_izg is not None:
            self.setWindowTitle("Изменить")
            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.save)
            self.load()
            self.btn_del = QPushButton("Удалить")
            self.btnlayout.addWidget(self.btn_del)
            self.btn_del.clicked.connect(self.delete)

    def add(self):
        zavod_izg = VypZav()
        zavod_izg.name = self.zavod_izg_edit.text()
        zavod_izg.save()
        self.accept()

    def load(self):
        self.zavod_izg_edit.setText(self.zavod_izg.name)

    def save(self):
        self.zavod_izg.name = self.zavod_izg_edit.text()
        self.zavod_izg.save()
        self.accept()

    def delete(self):
        self.zavod_izg.not_delete = False
        self.zavod_izg.save()
        self.accept()


class AddZavodRem(Adds):
    def __init__(self, zavod_rem: RemZav = None, parent=None):
        super().__init__(parent)
        self.zavod_rem = zavod_rem
        self.setWindowTitle("Добавить ремонтный завод")
        self.zavod_rem_edit = QLineEdit()
        self.form.addRow("Ремонтный завод", self.zavod_rem_edit)
        if self.zavod_rem is not None:
            self.setWindowTitle("Изменить")
            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.save)
            self.load()
            self.btn_del = QPushButton("Удалить")
            self.btnlayout.addWidget(self.btn_del)
            self.btn_del.clicked.connect(self.delete)

    def add(self):
        zavod_rem = RemZav()
        zavod_rem.name = self.zavod_rem_edit.text()
        zavod_rem.save()
        self.accept()

    def load(self):
        self.zavod_rem_edit.setText(self.zavod_rem.name)

    def save(self):
        self.zavod_rem.name = self.zavod_rem_edit.text()
        self.zavod_rem.save()
        self.accept()

    def delete(self):
        self.zavod_rem.not_delete = False
        self.zavod_rem.save()
        self.accept()


class AddSpec(Adds):
    def __init__(self, spec: Spec = None, parent=None):
        super().__init__(parent)
        self.spec = spec
        self.setWindowTitle("Добавить специальность")
        self.spec_edit = QLineEdit()
        self.form.addRow("Специальность", self.spec_edit)
        if self.spec is not None:
            self.setWindowTitle("Изменить")
            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.save)
            self.load()
            self.btn_del = QPushButton("Удалить")
            self.btnlayout.addWidget(self.btn_del)
            self.btn_del.clicked.connect(self.delete)

    def add(self):
        spec = Spec()
        spec.name = self.spec_edit.text()
        spec.save()
        self.accept()

    def load(self):
        self.spec_edit.setText(self.spec.name)

    def save(self):
        self.spec.name = self.spec_edit.text()
        self.spec.save()
        self.accept()

    def delete(self):
        self.spec.not_delete = False
        self.spec.save()
        self.accept()


class AddTypeRem(Adds):
    def __init__(self, type_rem: RemType = None, parent=None):
        super().__init__(parent)
        self.type_rem = type_rem
        self.setWindowTitle("Добавить тип ремонта")
        self.type_rem_edit = QLineEdit()
        self.plane_type = TypePlaneComboBox(PlaneType.select().where(PlaneType.not_delete == True))
        self.form.addRow("Тип самолета", self.plane_type)
        self.form.addRow("&Наименование", self.type_rem_edit)
        if self.type_rem is not None:
            self.setWindowTitle("Изменить")
            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.save)
            self.load()
            self.btn_del = QPushButton("Удалить")
            self.btnlayout.addWidget(self.btn_del)
            self.btn_del.clicked.connect(self.delete)

    def add(self):
        type_rem = RemType()
        type_rem.name = self.type_rem_edit.text()
        type_rem.planeType = self.plane_type.currentData(Qt.ItemDataRole.UserRole)
        type_rem.save()
        self.accept()

    def load(self):
        self.type_rem_edit.setText(self.type_rem.name)
        self.plane_type.setCurrentIndex(self.plane_type.findData(self.type_rem.planeType.id))

    def save(self):
        self.type_rem.name = self.type_rem_edit.text()
        self.type_rem.planeType = self.plane_type.currentData(Qt.ItemDataRole.UserRole)
        self.type_rem.save()
        self.accept()

    def delete(self):
        self.type_rem.not_delete = False
        self.type_rem.save()
        self.accept()



