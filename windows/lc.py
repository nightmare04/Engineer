import datetime
from functools import partial

from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QGroupBox, QGridLayout, QDialog, QVBoxLayout, QWidget, \
    QFormLayout, QLineEdit, QDateEdit, QTextEdit

from custom_widgets.buttons import TypeBtn
from database.models import *
from custom_widgets.groupboxs import PlaneGroupBox
from custom_widgets.buttons import SpecBtn, PlaneBtn
from custom_widgets.tables import *
from custom_widgets.combobox import *


class ListLC(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.table = LCTableView()
        self.table.doubleClicked.connect(self.exec_lc)
        self.mainLayout.addWidget(self.table)

        self.filter_layout = QHBoxLayout()
        self.btn_filter_ex = QPushButton("Только не &выполненные")
        self.btn_filter_ex.setCheckable(True)
        self.btn_filter_ex.clicked.connect(lambda: self.set_filter_by_btn(1, self.btn_filter_ex))

        self.btn_filter_de = QPushButton("Только &просроченные")
        self.btn_filter_de.setCheckable(True)
        self.btn_filter_de.clicked.connect(lambda: self.set_filter_by_btn(2, self.btn_filter_de))

        self.filterPlaneCombo = PlaneFilterComboBox(Plane.select().where(Plane.not_delete == True))
        self.filterPlaneCombo.currentIndexChanged.connect(lambda index: self.set_filter_by_combo(index))
        self.filter_layout.addWidget(self.btn_filter_ex)
        self.filter_layout.addWidget(self.btn_filter_de)
        self.filter_layout.addWidget(self.filterPlaneCombo)
        self.mainLayout.addLayout(self.filter_layout)

        self.btn_layout = QHBoxLayout()
        self.btn_add_lc = QPushButton("Добавить")
        self.btn_add_lc.clicked.connect(self.add_lc_w)
        self.btn_layout.addWidget(self.btn_add_lc)
        self.mainLayout.addLayout(self.btn_layout)

    def set_filter_by_combo(self, index):
        data = self.filterPlaneCombo.itemData(index, role=Qt.ItemDataRole.DisplayRole)
        self.set_filter(data, 5)

    def set_filter_by_btn(self, case, btn):
        if case == 1 and btn.isChecked():
            self.set_filter("Не выполнено", 5)
            return
        if case == 2 and btn.isChecked():
            self.set_filter('Просрочен', 3)
            return
        if not btn.isChecked():
            self.set_filter('', 0)
            return

    def set_filter(self, data, col):
        if data == "Все":
            self.table.proxy_model.setFilterRegularExpression('')
        else:
            self.table.proxy_model.setFilterRegularExpression(data)
            self.table.proxy_model.setFilterKeyColumn(col)

    def add_lc_w(self):
        lcw = AddLC()
        if lcw.exec():
            self.table.model.updateData(ListControl.select())

    def exec_lc(self, item):
        lc_id = item.siblingAtColumn(6).data()
        exlcw = ExecLC(lc_id)
        if exlcw.exec():
            self.table.model.updateData(ListControl.select())


class ListControlWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lc = None
        self.resize(800, 600)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.formLayout = QFormLayout()
        self.tlgEdit = QLineEdit()
        self.tlgDateEdit = QDateEdit()
        self.tlgDateEdit.setDate(datetime.date.today())
        self.tlgDeadline = QDateEdit()
        self.tlgDeadline.setDate(datetime.date.today())
        self.lcNumber = QLineEdit()
        self.lcDescription = QTextEdit()
        self.formLayout.addRow("Номер указания/ТЛГ", self.tlgEdit)
        self.formLayout.addRow("Дата", self.tlgDateEdit)
        self.formLayout.addRow("Срок выполнения", self.tlgDeadline)
        self.formLayout.addRow("Номер листа контроля", self.lcNumber)
        self.formLayout.addRow("Краткое содержание", self.lcDescription)
        self.mainLayout.addLayout(self.formLayout)

        self.dynLayout = QVBoxLayout()
        self.specGroupbox = QGroupBox()
        self.specLayout = QHBoxLayout()
        self.specGroupbox.setLayout(self.specLayout)
        self.specGroupbox.setTitle("Специальности")
        self.unitGroupbox = QGroupBox()
        self.unitLayout = QHBoxLayout()
        self.unitGroupbox.setLayout(self.unitLayout)
        self.unitGroupbox.setTitle("Подразделения")
        self.dynLayout.addWidget(self.specGroupbox)
        self.dynLayout.addWidget(self.unitGroupbox)
        self.mainLayout.addLayout(self.dynLayout)

        self.btnLayout = QHBoxLayout()
        self.btnOk = QPushButton("Ок")
        self.btnCancel = QPushButton("Отмена")
        self.btnLayout.addWidget(self.btnOk)
        self.btnLayout.addWidget(self.btnCancel)
        self.mainLayout.addLayout(self.btnLayout)

        self.planeTypeGroupbox = QGroupBox()
        self.planeTypeGroupbox.setTitle("Типы самолетов")
        self.planeTypeGroupbox.setLayout(QHBoxLayout())

    def type_select(self, type_btn: TypeBtn):
        planes_btns = self.findChildren(PlaneBtn)
        for btn in planes_btns:
            if type_btn.isChecked() and btn.plane.planeType.id == type_btn.type_plane.id:
                btn.setChecked(True)
            else:
                btn.setChecked(False)

    def add_lc(self):
        if self.lc is None:
            self.lc = ListControl()
        self.lc.tlg = self.tlgEdit.text()
        self.lc.tlgDate = self.tlgDateEdit.date().toPyDate()
        self.lc.lcNumber = self.lcNumber.text()
        self.lc.planes = self.dump_plane()
        self.lc.specs = self.dump_spec()
        self.lc.tlgDeadline = self.tlgDeadline.date().toPyDate()
        self.lc.description = self.lcDescription.toPlainText()
        self.lc.save()
        self.accept()

    def dump_spec(self):
        spec_on_create = []
        spec_to_exec = []
        specs_btns = self.specGroupbox.findChildren(SpecBtn)
        for spec_btn in specs_btns:
            spec_on_create.append(spec_btn.spec.id)
            if spec_btn.isChecked():
                spec_to_exec.append(spec_btn.spec.id)
        res = {}
        res.update({"on_create": spec_on_create})
        res.update({"to_exec": spec_to_exec})
        return res

    def dump_plane(self):
        plane_to_exec = {}
        plane_on_create = {}
        res = {}
        units_gb = self.unitGroupbox.findChildren(PlaneGroupBox)
        for unit_gb in units_gb:
            res_to_exec = []
            res_on_create = []
            planes_btns = unit_gb.findChildren(PlaneBtn)
            for plane_btn in planes_btns:
                res_on_create.append(plane_btn.plane.id)
                if plane_btn.isChecked():
                    res_to_exec.append(plane_btn.plane.id)
            if res_to_exec:
                plane_to_exec.update({unit_gb.unit.id: res_to_exec})
            plane_on_create.update({unit_gb.unit.id: res_on_create})

        res.update({"on_create": plane_on_create})
        res.update({"to_exec": plane_to_exec})

        return res


class AddLC(ListControlWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить Лист контроля")
        self.btnOk.clicked.connect(partial(self.add_lc))
        self.btnCancel.clicked.connect(self.reject)
        self.fill_form()

    def fill_form(self):
        if len(PlaneType.select().where(PlaneType.not_delete == True)) > 1:
            self.type_fill()
        self.spec_fill()
        self.unit_fill()

    def type_fill(self):
        types = PlaneType.select().where(PlaneType.not_delete == True)
        for plane_type in types:
            btn = TypeBtn(plane_type)
            btn.setCheckable(True)
            btn.setStyleSheet("TypeBtn{background-color: red;}"
                              "TypeBtn:checked{background-color: green;}")
            btn.clicked.connect(partial(self.type_select, btn))
            self.planeTypeGroupbox.layout().addWidget(btn)
        self.dynLayout.insertWidget(0, self.planeTypeGroupbox)

    def spec_fill(self):
        specs = Spec.select().where(Spec.not_delete == True)
        for spec in specs:
            btn_spec = SpecBtn(spec)
            self.specLayout.addWidget(btn_spec)

    def unit_fill(self):
        for unit in Unit.select().where(Unit.not_delete == True):
            i = 0
            j = 0
            unit_groupbox = PlaneGroupBox(unit, True, self.unitGroupbox)
            unit_lout = QGridLayout()
            unit_groupbox.setLayout(unit_lout)
            for plane in Plane.select().join(Unit).where(Plane.unit == unit.id, Plane.not_delete == True):
                i += 1
                btn_plane = PlaneBtn(plane)
                btn_plane.setChecked(True)
                unit_lout.addWidget(btn_plane, j, i)
                if i > 2:
                    j += 1
                    i = 0
            self.unitLayout.addWidget(unit_groupbox)


class EditLC(ListControlWindow):
    def __init__(self, lc: ListControl, parent=None):
        super().__init__(parent)
        self.lc = lc
        self.setWindowTitle("Изменить Лист контроля")
        self.btnOk.clicked.connect(partial(self.add_lc))
        self.btnCancel.clicked.connect(self.reject)
        self.btnDelete = QPushButton("Удалить")
        self.btnLayout.addWidget(self.btnDelete)
        self.btnDelete.clicked.connect(self.delete_lc)
        self.fill_form()

    def delete_lc(self):
        self.lc.delete_instance()
        self.accept()

    def fill_form(self):
        self.spec_load()
        self.unit_fill()
        self.load_lc()

    def load_lc(self):
        self.tlgEdit.setText(self.lc.tlg)
        self.tlgDateEdit.setDate(self.lc.tlgDate)
        self.tlgDeadline.setDate(self.lc.tlgDeadline)
        self.lcNumber.setText(self.lc.lcNumber)
        self.lcDescription.setText(self.lc.description)

    def spec_load(self):
        specs_id = self.lc.specs
        for spec_id in specs_id["on_create"]:
            spec = Spec.get_by_id(spec_id)
            spec_btn = SpecBtn(spec)
            spec_btn.setChecked(self.check_spec(spec_btn))
            self.specLayout.addWidget(spec_btn)

    def unit_fill(self):
        for unit_id in self.lc.planes["on_create"].keys():
            unit = Unit.get_by_id(unit_id)
            i = 0
            j = 0
            unit_groupbox = PlaneGroupBox(unit, True, self.unitGroupbox)
            unit_lout = QGridLayout()
            unit_groupbox.setLayout(unit_lout)
            for plane_id in self.lc.planes["on_create"][unit_id]:
                plane = Plane.get_by_id(plane_id)
                i += 1
                if plane.not_delete:
                    btn_plane = PlaneBtn(plane)
                    btn_plane.setChecked(self.check_plane(btn_plane))
                    unit_lout.addWidget(btn_plane, j, i)
                    if i > 2:
                        j += 1
                        i = 0
            self.unitLayout.addWidget(unit_groupbox)

    def check_plane(self, plane_btn: PlaneBtn) -> bool:
        planes_to_exec = self.lc.planes["to_exec"].values()
        all_planes = []
        for planes_unit in planes_to_exec:
            for plane in planes_unit:
                all_planes.append(plane)

        for plane in all_planes:
            if plane == plane_btn.plane.id:
                return True
        return False

    def check_spec(self, spec_btn: SpecBtn) -> bool:
        specs_to_exec = self.lc.specs["to_exec"]
        for spec in specs_to_exec:
            if spec == spec_btn.spec.id:
                return True
        return False


class ExecLC(QDialog):
    def __init__(self, lc_id, parent=None):
        super().__init__(parent)
        self.lc = ListControl.get_by_id(lc_id)
        self.resize(600, 250)
        self.setWindowTitle('Отметь выполненные самолеты')
        self.globalLayout = QVBoxLayout()
        self.setLayout(self.globalLayout)
        self.unitLayout = QHBoxLayout()
        self.globalLayout.addLayout(self.unitLayout)

        self.btn_layout = QHBoxLayout()
        self.btn_edit = QPushButton("Изменить")
        self.btn_delete = QPushButton("Удалить")
        self.btn_edit.clicked.connect(self.edit)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_layout.addWidget(self.btn_edit)
        self.btn_layout.addWidget(self.btn_delete)
        self.globalLayout.addLayout(self.btn_layout)

        self.unit_fill()
        self.btn_connect()
        self.plane_check()

    def edit(self):
        edit_lc_w = EditLC(self.lc)
        if edit_lc_w.exec():
            edit_lc_w.add_lc()
        self.accept()

    def delete(self):
        self.lc.delete_instance()
        self.accept()

    def btn_connect(self):
        for btn in self.findChildren(PlaneBtn):
            btn.clicked.connect(partial(self.open_exec_spec, btn.plane))

    def open_exec_spec(self, plane_btn):
        spec_window = ExecSpec(plane_btn, self.lc)
        spec_window.exec()
        btns = self.findChildren(PlaneBtn)
        for bnt in btns:
            bnt.check_exec(self.lc)

    def unit_fill(self):
        for unit in self.lc.planes["to_exec"].keys():
            i, j = 0, 0
            unit_groupbox = PlaneGroupBox(Unit.get(Unit.id == unit))
            unit_lout = QGridLayout()
            unit_groupbox.setLayout(unit_lout)
            planes = self.lc.planes["to_exec"][unit]
            for plane_id in planes:
                i += 1
                plane = Plane.get_by_id(plane_id)
                btn_plane = PlaneBtn(plane, self.lc)
                btn_plane.setCheckable(False)
                unit_lout.addWidget(btn_plane, j, i)
                if i > 2:
                    j += 1
                    i = 0
            self.unitLayout.addWidget(unit_groupbox)

    def plane_check(self):
        planes_btn = self.findChildren(PlaneBtn)
        for plane_btn in planes_btn:
            plane_btn.check_exec(self.lc)


class ExecSpec(QDialog):
    def __init__(self, plane: Plane, lc: ListControl, parent=None):
        super().__init__(parent)
        self.lc = lc
        self.plane = plane
        self.resize(300, 100)
        self.setWindowTitle('Отметь выполненные специальности')
        self.globalLayout = QVBoxLayout()
        self.setLayout(self.globalLayout)
        self.specLayout = QHBoxLayout()
        self.globalLayout.addLayout(self.specLayout)
        self.spec_fill(self.specLayout, self.lc)

    def spec_fill(self, layout, lc):
        specs = lc.specs["to_exec"]
        for spec in specs:
            spec_obj = Spec.get(spec)
            btn = SpecBtn(spec_obj, lc)
            btn.clicked.connect(partial(self.switch_spec, btn, self.lc.id, self.plane.id, spec_obj.id))
            spec_check = ListControlExec.get_or_none(
                lcId=self.lc.id,
                planeId=self.plane.id,
                specId=spec_obj.id
            )
            if spec_check is None:
                btn.setStyleSheet("background-color: red")
            else:
                btn.setStyleSheet("background-color: green")
            layout.addWidget(btn)

    @staticmethod
    def switch_spec(btn, lc_id, plane_id, spec_id):
        res = ListControlExec.get_or_create(
            lcId=lc_id,
            planeId=plane_id,
            specId=spec_id,
            defaults={'date': datetime.date.today()}
        )
        if not res[1]:
            res[0].delete_instance()
            btn.setStyleSheet("background-color: red")
        else:
            btn.setStyleSheet("background-color: green")
