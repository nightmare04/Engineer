import datetime
from functools import partial

from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QGroupBox, QGridLayout, QDialog, QVBoxLayout

from custom_widgets.buttons import TypeBtn
from database.lc import add_lc
from ui import Ui_D_add_lk
from database.models import *
from custom_widgets.groupboxs import PlaneGroupBox
from custom_widgets.buttons import SpecBtn, PlaneBtn


class AddLC(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_D_add_lk()
        self.ui.setupUi(self)
        self.setWindowTitle("Добавить Лист контроля")
        self.ui.btn_ok.clicked.connect(self.accept)
        self.ui.btn_cancel.clicked.connect(self.reject)

        self.plane_type_gb = QGroupBox()
        self.plane_type_gb.setTitle("Типы самолетов")
        self.plane_type_gb.setLayout(QHBoxLayout())

        self.fill_form()
        self.ui.tlgDateEdit.setDate(datetime.date.today())
        self.ui.tlgDeadlineEdit.setDate((datetime.date.today()))

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
            self.plane_type_gb.layout().addWidget(btn)
        self.ui.verticalLayout.insertWidget(0, self.plane_type_gb)

    def type_select(self, type_btn: TypeBtn):
        planes_btns = self.findChildren(PlaneBtn)
        for btn in planes_btns:
            if type_btn.isChecked() and btn.plane.planeType.id == type_btn.type_plane.id:
                btn.setChecked(True)
            else:
                btn.setChecked(False)

    def spec_fill(self):
        specs = Spec.select().where(Spec.not_delete == True)
        for spec in specs:
            btn_spec = SpecBtn(spec)
            self.ui.spec_layout.addWidget(btn_spec)

    def unit_fill(self):
        for unit in Unit.select().where(Unit.not_delete == True):
            i = 0
            j = 0
            unit_groupbox = PlaneGroupBox(unit, True, self.ui.podr_groupbox)
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
            self.ui.unit_layout.addWidget(unit_groupbox)


class EditLC(QDialog):
    def __init__(self, lc: ListControl, parent=None):
        self.lc = lc
        super().__init__(parent)
        self.ui = Ui_D_add_lk()
        self.ui.setupUi(self)
        self.setWindowTitle("Изменить Лист контроля")
        self.ui.btn_ok.clicked.connect(self.accept)
        self.ui.btn_cancel.clicked.connect(self.reject)
        self.delete_btn = QPushButton("Удалить")
        self.ui.horizontalLayout.addWidget(self.delete_btn)
        self.delete_btn.clicked.connect(self.delete_lc)
        self.fill_form()

    def delete_lc(self):
        self.lc.delete_instance()
        self.accept()

    def fill_form(self):
        self.spec_fill()
        self.unit_fill()
        self.load_lc()

    def load_lc(self):
        self.ui.lcEdit.setText(self.lc.lcNumber)
        self.ui.tlgDateEdit.setDate(self.lc.tlgDate)
        self.ui.tlgDeadlineEdit.setDate(self.lc.tlgDeadline)
        self.ui.textEdit.setText(self.lc.description)
        self.ui.tlgEdit.setText(self.lc.tlg)

    def spec_fill(self):
        specs_id = self.lc.specs
        for spec_id in specs_id["on_create"]:
            spec = Spec.get_by_id(spec_id)
            spec_btn = SpecBtn(spec)
            spec_btn.setChecked(self.check_spec(spec_btn))
            self.ui.spec_layout.addWidget(spec_btn)

    def unit_fill(self):
        for unit_id in self.lc.planes["on_create"].keys():
            unit = Unit.get_by_id(unit_id)
            i = 0
            j = 0
            unit_groupbox = PlaneGroupBox(unit, True, self.ui.podr_groupbox)
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
            self.ui.unit_layout.addWidget(unit_groupbox)

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
            add_lc(edit_lc_w, edit_lc_w.lc)
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
