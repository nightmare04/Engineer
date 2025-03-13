from PyQt6.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QFormLayout, QLineEdit, QDateEdit, QSpinBox

from custom_widgets.buttons import OsobBtn
from custom_widgets.combobox import *
from custom_widgets.groupboxs import OsobGroupBox
from database.models import *


class Adds(QDialog):
    update_signal = pyqtSignal()

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

        self.btn_ok.clicked.connect(self.save)
        self.btn_cancel.clicked.connect(self.reject)


class AddUnit(Adds):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.unit = None
        self.setWindowTitle("Добавить подразделение")
        self.unit_name = QLineEdit()
        self.form.addRow("Подразделение", self.unit_name)
        self.unit_name.setFocus()

    @pyqtSlot()
    def open_add(self):
        self.unit = Unit()
        self.exec()

    def save(self):
        self.unit.name = self.unit_name.text()
        self.unit.save()
        self.update_signal.emit()
        self.accept()

    @pyqtSlot(str)
    def open_edit(self, unit_id):
        self.unit = Unit.get_by_id(unit_id)
        self.unit_name.setText(self.unit.name)
        self.setWindowTitle("Изменить подразделение")
        self.btn_del = QPushButton("Удалить")
        self.btn_del.clicked.connect(self.delete)
        self.btnlayout.addWidget(self.btn_del)
        self.btn_ok.setText("Сохранить")
        self.btn_ok.clicked.disconnect()
        self.btn_ok.clicked.connect(self.save)
        self.exec()

    def clear(self):
        self.unit_name.setText("")

    def delete(self):
        self.unit.not_delete = False
        self.unit.save()
        self.update_signal.emit()
        self.accept()


class AddPlaneType(Adds):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.plane_type = None
        self.setWindowTitle("Добавить тип самолета")
        self.type_name = QLineEdit()
        self.form.addRow("Тип", self.type_name)
        self.type_name.setFocus()

    @pyqtSlot()
    def open_add(self):
        self.plane_type = PlaneType()
        self.exec()

    @pyqtSlot(str)
    def open_edit(self, plane_type_id):
        self.plane_type = PlaneType.get_by_id(plane_type_id)
        self.type_name.setText(self.plane_type.name)
        self.setWindowTitle("Изменить тип самолета")
        self.btn_del = QPushButton("Удалить")
        self.btn_del.clicked.connect(self.delete)
        self.btnlayout.addWidget(self.btn_del)
        self.btn_ok.setText("Сохранить")
        self.btn_ok.clicked.disconnect()
        self.btn_ok.clicked.connect(self.save)
        self.exec()

    def save(self):
        self.plane_type.name = self.type_name.text()
        self.plane_type.save()
        self.update_signal.emit()
        self.accept()

    def delete(self):
        self.plane_type.not_delete = False
        self.plane_type.save()
        self.update_signal.emit()
        self.accept()


class AddPlane(Adds):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.plane = None
        self.setWindowTitle("Добавить самолет")
        self.planeType_combobox = TypePlaneComboBox(PlaneType.select().where(PlaneType.not_delete == True))
        self.unit_combobox = UnitComboBox(Unit.select().where(Unit.not_delete == True))
        self.bortNum = QLineEdit()
        self.zavNum = QLineEdit()
        self.dateVyp = QDateEdit()
        self.vypZav = ZavodIzgComboBox(ZavIzg.select().where(ZavIzg.not_delete == True))
        self.dateRem = QDateEdit()
        self.remZav = RemZavComboBox(RemZav.select().where(RemZav.not_delete == True))
        self.remType = RemTypeComboBox(RemType.select().where(RemType.not_delete == True))
        self.osobPlane = OsobGroupBox()
        self.planeType_combobox.currentIndexChanged.connect(self.osob_fill)
        self.osob_fill()

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

        self.bortNum.setFocus()

    def open_add(self):
        self.plane = Plane()
        self.exec()

    @pyqtSlot(str)
    def open_edit(self, plane_id):
        self.plane = Plane.get_by_id(plane_id)
        self.load()
        self.setWindowTitle("Изменить самолет")
        self.btn_ok.setText("Сохранить")
        self.btn_ok.clicked.disconnect()
        self.btn_ok.clicked.connect(self.update_plane)
        self.btn_del = QPushButton("Удалить")
        self.btnlayout.addWidget(self.btn_del)
        self.btn_del.clicked.connect(self.delete)
        self.exec()

    def load(self):
        self.bortNum.setText(self.plane.name)
        self.zavNum.setText(self.plane.zavNum)
        self.planeType_combobox.setCurrentIndex(self.planeType_combobox.findData(str(self.plane.typeId)))
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

    def save(self):
        self.plane.typeId = self.planeType_combobox.currentData()
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
        self.update_signal.emit()
        self.accept()

    def delete(self):
        self.plane.not_delete = False
        self.plane.save()
        self.update_signal.emit()
        self.accept()

    def osob_fill(self):
        btns = self.osobPlane.findChildren(OsobBtn)
        for btn in btns:
            btn.setParent(None)
        i = 0
        j = 0
        for osob in OsobPlane.select().where(OsobPlane.not_delete == True, OsobPlane.typeId == self.planeType_combobox.currentData(Qt.ItemDataRole.UserRole)):
            i += 1
            btn_osob = OsobBtn(osob)
            self.osobPlane.mainlayout.addWidget(btn_osob, j, i)
            if i > 2:
                j += 1
                i = 0

    def osob_dump(self):
        res = []
        for osob_btn in self.findChildren(OsobBtn):
            if osob_btn.isChecked():
                res.append(osob_btn.osob_plane.id)
        return res


class AddOsob(Adds):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.osob = None
        self.setWindowTitle("Добавить особенность")
        self.osob_edit = QLineEdit()
        self.plane_type = TypePlaneComboBox(PlaneType.select().where(PlaneType.not_delete == True))
        self.form.addRow("Тип самолета", self.plane_type)
        self.form.addRow("&Наименование", self.osob_edit)
        self.osob_edit.setFocus()

    @pyqtSlot()
    def open_add(self):
        self.osob = OsobPlane()
        self.exec()

    @pyqtSlot(str)
    def open_edit(self, osob_id):
        self.osob = OsobPlane.get_by_id(osob_id)
        self.load()
        self.setWindowTitle("Изменить")
        self.btn_ok.setText("Сохранить")
        self.btn_ok.clicked.disconnect()
        self.btn_ok.clicked.connect(self.save)
        self.btn_del = QPushButton("Удалить")
        self.btnlayout.addWidget(self.btn_del)
        self.btn_del.clicked.connect(self.delete)
        self.exec()

    def load(self):
        self.osob_edit.setText(self.osob.name)
        self.plane_type.setCurrentIndex(self.plane_type.findData(self.osob.typeId.id))

    def save(self):
        self.osob.name = self.osob_edit.text()
        self.osob.typeId = self.plane_type.currentData(Qt.ItemDataRole.UserRole)
        self.osob.save()
        self.update_signal.emit()
        self.accept()

    def delete(self):
        self.osob.not_delete = False
        self.osob.save()
        self.update_signal.emit()
        self.accept()


class AddSystem(Adds):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.system = PlaneSystem()
        self.setWindowTitle("Добавить систему самолета")
        self.system_edit = QLineEdit()
        self.spec = SpecComboBox(Spec.select().where(Spec.not_delete == True))
        self.plane_type = TypePlaneComboBox(PlaneType.select().where(PlaneType.not_delete == True))
        self.form.addRow("Тип самолета", self.plane_type)
        self.form.addRow("Специальность", self.spec)
        self.form.addRow("Название системы", self.system_edit)
        self.system_edit.setFocus()

    @pyqtSlot()
    def open_add(self):
        self.system = PlaneSystem()
        self.exec()

    @pyqtSlot(str)
    def open_edit(self, system):
        self.system = PlaneSystem.get_by_id(system)
        self.load()
        self.setWindowTitle("Изменить")
        self.btn_ok.setText("Сохранить")
        self.btn_ok.clicked.disconnect()
        self.btn_ok.clicked.connect(self.save)
        self.btn_del = QPushButton("Удалить")
        self.btnlayout.addWidget(self.btn_del)
        self.btn_del.clicked.connect(self.delete)
        self.system_edit.setFocus()
        self.exec()

    def load(self):
        self.system_edit.setText(self.system.name)
        self.spec.setCurrentIndex(self.spec.findData(self.system.specId.id, role=Qt.ItemDataRole.UserRole))
        self.plane_type.setCurrentIndex(self.plane_type.findData(self.system.typeId.id, role=Qt.ItemDataRole.UserRole))

    def save(self):
        self.system.name = self.system_edit.text()
        self.system.specId = self.spec.currentData(role=Qt.ItemDataRole.UserRole)
        self.system.typeId = self.plane_type.currentData(role=Qt.ItemDataRole.UserRole)
        self.system.save()
        self.update_signal.emit()
        self.accept()

    def delete(self):
        self.system.not_delete = False
        self.system.save()
        self.update_signal.emit()
        self.accept()


class AddZavodIzg(Adds):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.zavod_izg = None
        self.setWindowTitle("Добавить завод изготовитель")
        self.zavod_izg_edit = QLineEdit()
        self.form.addRow("Завод изготовитель", self.zavod_izg_edit)
        self.zavod_izg_edit.setFocus()

    @pyqtSlot()
    def open_add(self):
        self.zavod_izg = ZavIzg()
        self.exec()

    @pyqtSlot(str)
    def open_edit(self, zavod_izg_id):
        self.zavod_izg = ZavIzg.get_by_id(zavod_izg_id)
        self.load()
        self.setWindowTitle("Изменить")
        self.btn_ok.setText("Сохранить")
        self.btn_ok.clicked.disconnect()
        self.btn_ok.clicked.connect(self.save)
        self.btn_del = QPushButton("Удалить")
        self.btnlayout.addWidget(self.btn_del)
        self.btn_del.clicked.connect(self.delete)
        self.exec()

    def load(self):
        self.zavod_izg_edit.setText(self.zavod_izg.name)

    def save(self):
        self.zavod_izg.name = self.zavod_izg_edit.text()
        self.zavod_izg.save()
        self.update_signal.emit()
        self.accept()

    def delete(self):
        self.zavod_izg.not_delete = False
        self.zavod_izg.save()
        self.update_signal.emit()
        self.accept()


class AddZavodRem(Adds):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.zavod_rem = None
        self.setWindowTitle("Добавить ремонтный завод")
        self.zavod_rem_edit = QLineEdit()
        self.form.addRow("Ремонтный завод", self.zavod_rem_edit)
        self.zavod_rem_edit.setFocus()

    def add(self):
        zavod_rem = RemZav()
        zavod_rem.name = self.zavod_rem_edit.text()
        zavod_rem.save()
        self.update_signal.emit()
        self.accept()

    @pyqtSlot(str)
    def open_edit(self, zavod_rem_id):
        self.zavod_rem = RemZav.get_by_id(zavod_rem_id)
        self.load()
        self.setWindowTitle("Изменить")
        self.btn_ok.setText("Сохранить")
        self.btn_ok.clicked.disconnect()
        self.btn_ok.clicked.connect(self.save)
        self.btn_del = QPushButton("Удалить")
        self.btnlayout.addWidget(self.btn_del)
        self.btn_del.clicked.connect(self.delete)
        self.exec()

    def load(self):
        self.zavod_rem_edit.setText(self.zavod_rem.name)

    def save(self):
        self.zavod_rem.name = self.zavod_rem_edit.text()
        self.zavod_rem.save()
        self.update_signal.emit()
        self.accept()

    def delete(self):
        self.zavod_rem.not_delete = False
        self.zavod_rem.save()
        self.update_signal.emit()
        self.accept()


class AddSpec(Adds):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.spec = None
        self.setWindowTitle("Добавить специальность")
        self.spec_edit = QLineEdit()
        self.form.addRow("Специальность", self.spec_edit)
        self.spec_edit.setFocus()

    def add(self):
        spec = Spec()
        spec.name = self.spec_edit.text()
        spec.save()
        self.update_signal.emit()
        self.accept()

    @pyqtSlot(str)
    def open_edit(self, spec_id):
        self.spec = Spec.get_by_id(spec_id)
        self.load()
        self.setWindowTitle("Изменить")
        self.btn_ok.setText("Сохранить")
        self.btn_ok.clicked.disconnect()
        self.btn_ok.clicked.connect(self.save)
        self.btn_del = QPushButton("Удалить")
        self.btnlayout.addWidget(self.btn_del)
        self.btn_del.clicked.connect(self.delete)
        self.exec()

    def load(self):
        self.spec_edit.setText(self.spec.name)

    def save(self):
        self.spec.name = self.spec_edit.text()
        self.spec.save()
        self.update_signal.emit()
        self.accept()

    def delete(self):
        self.spec.not_delete = False
        self.spec.save()
        self.update_signal.emit()
        self.accept()


class AddTypeRem(Adds):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.type_rem = None
        self.setWindowTitle("Добавить тип ремонта")
        self.type_rem_edit = QLineEdit()
        self.plane_type = TypePlaneComboBox(PlaneType.select().where(PlaneType.not_delete == True))
        self.form.addRow("Тип самолета", self.plane_type)
        self.form.addRow("&Наименование", self.type_rem_edit)
        self.type_rem_edit.setFocus()

    def add(self):
        type_rem = RemType()
        type_rem.name = self.type_rem_edit.text()
        type_rem.typeId = self.plane_type.currentData(Qt.ItemDataRole.UserRole)
        type_rem.save()
        self.update_signal.emit()
        self.accept()

    @pyqtSlot(str)
    def open_edit(self, type_rem_id):
        self.type_rem = RemType.get_by_id(type_rem_id)
        self.load()
        self.setWindowTitle("Изменить")
        self.btn_ok.setText("Сохранить")
        self.btn_ok.clicked.disconnect()
        self.btn_ok.clicked.connect(self.save)
        self.btn_del = QPushButton("Удалить")
        self.btnlayout.addWidget(self.btn_del)
        self.btn_del.clicked.connect(self.delete)
        self.exec()

    def load(self):
        self.type_rem_edit.setText(self.type_rem.name)
        self.plane_type.setCurrentIndex(self.plane_type.findData(self.type_rem.typeId.id))

    def save(self):
        self.type_rem.name = self.type_rem_edit.text()
        self.type_rem.typeId = self.plane_type.currentData(Qt.ItemDataRole.UserRole)
        self.type_rem.save()
        self.update_signal.emit()
        self.accept()

    def delete(self):
        self.type_rem.not_delete = False
        self.type_rem.save()
        self.update_signal.emit()
        self.accept()


class AddAgregateState(Adds):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.agregate_state = None
        self.setWindowTitle("Добавить состояние")
        self.agregate_state_edit = QLineEdit()
        self.form.addRow("&Наименование", self.agregate_state_edit)
        self.agregate_state_edit.setFocus()

    def add(self):
        agregate_state = AgregateState()
        agregate_state.name = self.agregate_state_edit.text()
        agregate_state.save()
        self.update_signal.emit()
        self.accept()

    @pyqtSlot(str)
    def open_edit(self, type_rem_id):
        self.agregate_state = AgregateState.get_by_id(type_rem_id)
        self.load()
        self.setWindowTitle("Изменить")
        self.btn_ok.setText("Сохранить")
        self.btn_ok.clicked.disconnect()
        self.btn_ok.clicked.connect(self.save)
        self.btn_del = QPushButton("Удалить")
        self.btnlayout.addWidget(self.btn_del)
        self.btn_del.clicked.connect(self.delete)
        self.exec()

    def load(self):
        self.agregate_state_edit.setText(self.agregate_state.name)

    def save(self):
        self.agregate_state.name = self.agregate_state_edit.text()
        self.agregate_state.save()
        self.update_signal.emit()
        self.accept()

    def delete(self):
        self.agregate_state.not_delete = False
        self.agregate_state.save()
        self.update_signal.emit()
        self.accept()


class AddAgregateName(Adds):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.agregate_name = None
        self.setWindowTitle("Добавить блок/агрегат")
        self.plane_type_cb = TypePlaneComboBox(PlaneType.select().where(PlaneType.not_delete == True))
        self.spec_cb = SpecComboBox(Spec.select().where(Spec.not_delete == True))
        self.system_cb = SystemComboBox(PlaneSystem.select().where(PlaneSystem.not_delete == True))
        self.count_on_plane = QSpinBox()
        self.count_on_plane.setValue(1)
        self.agregate_name_edit = QLineEdit()
        self.form.addRow("Тип самолета", self.plane_type_cb)
        self.form.addRow("Специальность", self.spec_cb)
        self.form.addRow("Система", self.system_cb)
        self.form.addRow("Наименование", self.agregate_name_edit)
        self.form.addRow("Количество на самолете", self.count_on_plane)
        self.agregate_name_edit.setFocus()
        self.plane_type_cb.currentTextChanged.connect(self.changeData)
        self.spec_cb.currentTextChanged.connect(self.changeData)
        self.changeData()
        self.agregate_name_edit.setFocus()

    def changeData(self):
        self.system_cb.model.updateData(
            (PlaneSystem.select().where(PlaneSystem.specId == self.spec_cb.currentData(Qt.ItemDataRole.UserRole),
                                        PlaneSystem.typeId == self.plane_type_cb.currentData(
                                            Qt.ItemDataRole.UserRole))))

    def add(self):
        self.agregate_name = AgregateName()
        self.agregate_name.name = self.agregate_name_edit.text()
        self.agregate_name.typeId = self.plane_type_cb.currentData(Qt.ItemDataRole.UserRole)
        self.agregate_name.specId = self.spec_cb.currentData(Qt.ItemDataRole.UserRole)
        self.agregate_name.systemId = self.system_cb.currentData(Qt.ItemDataRole.UserRole)
        self.agregate_name.count_on_plane = self.count_on_plane.value()
        self.agregate_name.save()
        self.update_signal.emit()
        self.accept()

    @pyqtSlot(str)
    def open_edit(self, type_rem_id):
        self.agregate_name = AgregateName.get_by_id(type_rem_id)
        self.load()
        self.setWindowTitle("Изменить")
        self.btn_ok.setText("Сохранить")
        self.btn_ok.clicked.disconnect()
        self.btn_ok.clicked.connect(self.save)
        self.btn_del = QPushButton("Удалить")
        self.btnlayout.addWidget(self.btn_del)
        self.btn_del.clicked.connect(self.delete)
        self.exec()

    def load(self):
        self.agregate_name_edit.setText(self.agregate_name.name)
        self.plane_type_cb.setCurrentIndex(self.plane_type_cb.findText(self.agregate_name.typeId.name))
        self.spec_cb.setCurrentIndex(self.spec_cb.findText(self.agregate_name.specId.name))
        self.system_cb.setCurrentIndex(self.system_cb.findText(self.agregate_name.systemId.name))
        self.count_on_plane.setValue(self.agregate_name.count_on_plane)

    def save(self):
        self.agregate_name.name = self.agregate_name_edit.text()
        self.agregate_name.typeId = self.plane_type_cb.currentData(Qt.ItemDataRole.UserRole)
        self.agregate_name.specId = self.spec_cb.currentData(Qt.ItemDataRole.UserRole)
        self.agregate_name.systemId = self.system_cb.currentData(Qt.ItemDataRole.UserRole)
        self.agregate_name.count_on_plane = self.count_on_plane.text()
        self.agregate_name.save()
        self.update_signal.emit()
        self.accept()

    def delete(self):
        self.agregate_name.not_delete = False
        self.agregate_name.save()
        self.update_signal.emit()
        self.accept()


class AddAgregate(Adds):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.plane_type = Plane()
        self.agregate = AgregateOnPlane()
        self.spec_cb = SpecComboBox(Spec.select().where(Spec.not_delete == True))
        self.system_cb = SystemComboBox(PlaneSystem.select().where(PlaneSystem.not_delete == True))
        self.agregate_cb = AgregateComboBox(AgregateOnPlane.select().where(AgregateOnPlane.agregateId.systemId == self.system_cb.currentData(Qt.ItemDataRole.UserRole)))
        self.agregate_zavnum = QLineEdit()
        self.agregate_date = QDateEdit()
        self.agregate_state = StateComboBox(AgregateState.select().where(AgregateState.not_delete == True))
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Добавить блок/агрегат")
        self.form.addRow("Специальность", self.spec_cb)
        self.form.addRow("Система", self.system_cb)
        self.form.addRow("Наименование", self.agregate)
        self.form.addRow("Заводской номер", self.agregate_zavnum)
        self.form.addRow("Дата выпуска", self.agregate_date)
        self.form.addRow("Состояние", self.agregate_state)
        self.system_cb.currentTextChanged.connect(self.changeData)

    @pyqtSlot(Plane)
    def open_add(self, plane):
        self.plane = plane
        self.changeData()
        self.exec()

    @pyqtSlot(str)
    def open_edit(self, agregate_id):
        self.agregate = AgregateOnPlane.get_by_id(agregate_id)
        self.setWindowTitle("Изменить")
        self.btn_ok.setText("Сохранить")
        self.btn_ok.clicked.disconnect()
        self.btn_ok.clicked.connect(self.save)
        self.btn_del = QPushButton("Удалить")
        self.btnlayout.addWidget(self.btn_del)
        self.btn_del.clicked.connect(self.delete)
        self.spec_cb.setCurrentIndex(self.spec_cb.findText(self.agregate.agregateId.specId))
        self.system_cb.setCurrentIndex(self.system_cb_cb.findText(self.agregate.agregateId.systemId))
        self.agregate_zavnum.setText(self.agregate.zavNum)
        self.agregate_date.setDate(self.agregate.dateVyp)
        self.agregate_state.setCurrentIndex(self.agregate_state.findData(self.agregate.state, Qt.ItemDataRole.UserRole))
        self.exec()

    def changeData(self):
        self.agregate.model.updateData(AgregateOnPlane.select().
                                       where(AgregateOnPlane.agregateId.systemId ==
                                             self.system_cb.currentData(Qt.ItemDataRole.UserRole)))

    def save(self):
        self.agregate.agregateId = self.agregate_cb.currentData(Qt.ItemDataRole.UserRole)
        self.agregate.zavNum = self.agregate_zavnum.text()
        self.agregate.state = self.agregate_state.currentData(Qt.ItemDataRole.UserRole)
        self.agregate.save()
        self.update_signal.emit()
        self.accept()

    def delete(self):
        self.agregate.delete_instance()
        self.update_signal.emit()
        self.accept()
