from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QGroupBox, QGridLayout, QDialog, QVBoxLayout

from ui import Ui_D_add_lk
from database import *
from custom_widgets import *


class BaseLC:
    def spec_fill(self, spec_lout, lc: ListControl = None, plane: Plane = None):
        if lc and plane is None:
            specs = Spec.select(Spec.name).tuples()
            for spec in specs:
                btn_spec = SpecBtn(spec)
                spec_lout.addWidget(btn_spec)
        else:
            specs = lc.spec_for_exec
            for spec_str in specs:
                spec = Spec.get(Spec.name == spec_str)
                btn_spec = SpecBtn(spec.name)
                btn_spec.clicked.connect(lambda: self.exec_spec(lc, plane, spec))
                spec_lout.addWidget(btn_spec)

    @staticmethod
    def exec_spec(lc: ListControl, plane: Plane, spec: Spec):
        res = ListControlExec.select().where(
            (ListControlExec.id_lk == lc.id) &
            (ListControlExec.plane == plane.id))
        print(res)

    @staticmethod
    def unit_fill_new(gb):
        for unit in Unit.select():
            i = 0
            j = 0
            unit_groupbox = PlaneGroupBox(unit, True, gb)
            unit_lout = QGridLayout()
            unit_groupbox.setLayout(unit_lout)
            for plane in Plane.select().join(Unit).where(Plane.unit == unit.id):
                i += 1
                btn_plane = PlaneBtn(plane.bort_num)
                btn_plane.setChecked(True)
                unit_lout.addWidget(btn_plane, j, i)
                if i > 2:
                    j += 1
                    i = 0
            gb.layout().addWidget(unit_groupbox)

    @staticmethod
    def unit_fill(lc_id, gb):
        lc = ListControl.get_by_id(lc_id)
        for unit in lc.planes_for_exec.keys():
            i, j = 0, 0
            unit_groupbox = PlaneGroupBox(Unit.get(Unit.name == unit))
            unit_lout = QGridLayout()
            unit_groupbox.setLayout(unit_lout)
            planes = lc.planes_for_exec[unit]
            for plane in planes:
                i += 1
                btn_plane = PlaneBtn(plane)
                btn_plane.setChecked(True)
                unit_lout.addWidget(btn_plane, j, i)
                if i > 2:
                    j += 1
                    i = 0
            gb.layout().addWidget(unit_groupbox)


class AddLC(QDialog, BaseLC):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_D_add_lk()
        self.ui.setupUi(self)
        self.setWindowTitle("Добавить Лист контроля")
        self.spec_lout = QHBoxLayout()
        self.ui.spec_groupbox.setLayout(self.spec_lout)
        self.unit_lout = QHBoxLayout()
        self.ui.podr_groupbox.setLayout(self.unit_lout)
        self.ui.btn_ok.clicked.connect(self.accept)
        self.ui.btn_cancel.clicked.connect(self.reject)
        self.fill_form()

    def fill_form(self):
        self.spec_fill(self.spec_lout)
        self.unit_fill_new(self.ui.podr_groupbox)


class EditLC(AddLC):
    def __init__(self, lc_id, parent=None):
        self.lc = ListControl.get_by_id(lc_id)
        super().__init__(parent)
        self.setWindowTitle("Изменить Лист контроля")

    def fill_form(self):
        self.spec_fill(self.spec_lout)
        self.unit_fill(lc_id, self.ui.podr_groupbox)


class ExecLC(QDialog, BaseLC):
    def __init__(self, lc_id, parent=None):
        super().__init__(parent)
        self.lc = ListControl.get_by_id(lc_id)
        self.resize(600, 250)
        self.setWindowTitle('Отметь выполненные самолеты')
        self.globalLayout = QVBoxLayout(self)
        self.setLayout(self.globalLayout)
        self.unitLayout = QHBoxLayout()
        self.globalLayout.addLayout(self.unitLayout)
        self.unit_fill(self.lc, self.unitLayout)
        self.btn_connect()

    def btn_connect(self):
        for btn in self.findChildren(PlaneBtn):
            btn.clicked.connect(lambda: self.open_exec_spec(btn.plane, self.lc.id))

    def open_exec_spec(self, plane, lc_id):
        spec_window = ExecSpec(plane, lc_id)
        spec_window.exec()
        self.unit_fill(self.ui.podr_groupbox, lc_id)


class ExecSpec(QDialog, BaseLC):
    def __init__(self, plane, lc_id, parent=None):
        super().__init__(parent)
        self.lc = ListControl.get_by_id(lc_id)
        self.resize(300, 100)
        self.setWindowTitle('Отметь выполненные специальности')
        self.globalLayout = QHBoxLayout(self)
        self.setLayout(self.globalLayout)
        self.spec_fill(self.globalLayout, self.lc)

