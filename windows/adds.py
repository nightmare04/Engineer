from functools import partial

from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, \
    QFormLayout, QComboBox, QLineEdit, QCheckBox, QDateEdit
from PyQt6.QtCore import Qt

from custom_widgets.buttons import OsobBtn
from custom_widgets.combobox import TypePlaneComboBox, UnitComboBox, RemZavComboBox, VypZavComboBox, RemTypeComboBox
from custom_widgets.groupboxs import OsobGroupBox
from database.models import PlaneType, Plane, Unit, Spec, RemType, RemZav, VypZav, OsobPlane


class Adds(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(500, 500)
        self.mainlayout = QVBoxLayout(self)
        self.setLayout(self.mainlayout)

        self.formlayout = QFormLayout()
        self.btnlayout = QHBoxLayout()

        self.btn_ok = QPushButton("Ок")
        self.btn_cancel = QPushButton("Отменить")
        self.btnlayout.addWidget(self.btn_ok)
        self.btnlayout.addWidget(self.btn_cancel)

        self.mainlayout.addLayout(self.formlayout)
        self.mainlayout.addLayout(self.btnlayout)

        self.btn_ok.clicked.connect(self.add)
        self.btn_cancel.clicked.connect(self.reject)

    def add(self):
        pass

    def delete(self, model):
        model.not_delete = False
        model.save()
        self.accept()


class AddAll(Adds):
    def __init__(self, basemodel, edit_item=None, parent=None):
        super().__init__(parent)
        self.instance = basemodel
        self.edit_item = edit_item
        self.setWindowTitle("Добавить")
        self.instance_edit = QLineEdit()
        self.formlayout.addRow("&Наименование", self.instance_edit)
        if edit_item is not None:
            self.setWindowTitle("Изменить")
            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.save)
            self.load(edit_item)
            self.btn_delete = QPushButton("Удалить")
            self.btnlayout.addWidget(self.btn_delete)
            self.btn_delete.clicked.connect(partial(self.delete, self.edit_item))

    def add(self):
        self.instance.create(name=self.instance_edit.text())
        self.instance_edit.setText("")

    def save(self):
        self.edit_item.name = self.instance_edit.text()
        self.edit_item.save()
        self.accept()

    def load(self, edit_item):
        self.instance_edit.setText(edit_item.name)


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

        self.formlayout.addRow("Тип самолета", self.planeType_combobox)
        self.formlayout.addRow("Подразделение", self.unit_combobox)
        self.formlayout.addRow("Бортовой номер", self.bortNum)
        self.formlayout.addRow("Заводской номер", self.zavNum)
        self.formlayout.addRow("Дата выпуска", self.dateVyp)
        self.formlayout.addRow("Завод изготовитель", self.vypZav)
        self.formlayout.addRow("Дата ремонта", self.dateRem)
        self.formlayout.addRow("АРЗ", self.remZav)
        self.formlayout.addRow("Вид ремонта", self.remType)
        self.formlayout.addRow("Особенности самолета", self.osobPlane)

        if self.plane is not None:
            self.setWindowTitle("Изменить самолет")
            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.update_plane)
            self.load()

            self.btn_del = QPushButton("Удалить")
            self.btnlayout.addWidget(self.btn_del)
            self.btn_del.clicked.connect(partial(self.delete, self.plane))

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


class AddOsob(Adds):
    def __init__(self, basemodel, osob: OsobPlane = None, parent=None):
        super().__init__(parent)
        self.instance = basemodel
        self.osob = osob
        self.setWindowTitle("Добавить особенность")
        self.osob_edit = QLineEdit()
        self.plane_type = TypePlaneComboBox(PlaneType.select().where(PlaneType.not_delete == True))
        self.formlayout.addRow("Тип самолета", self.plane_type)
        self.formlayout.addRow("&Наименование", self.osob_edit)
        if self.osob is not None:
            self.setWindowTitle("Изменить")
            self.btn_ok.setText("Сохранить")
            self.btn_ok.clicked.disconnect()
            self.btn_ok.clicked.connect(self.save)
            self.load()

            self.btn_del = QPushButton("Удалить")
            self.btnlayout.addWidget(self.btn_del)
            self.btn_del.clicked.connect(partial(self.delete, self.osob))

    def add(self):
        osob = OsobPlane()
        osob.name = self.osob_edit.text()
        osob.planeType = self.planeType.currentData(role=Qt.ItemDataRole.UserRole)
        osob.save()
        self.accept()

    def load(self):
        self.osob_edit.setText(self.osob.name)

    def save(self):
        self.osob.name = self.osob_edit.text()
        self.osob.save()
        self.accept()
