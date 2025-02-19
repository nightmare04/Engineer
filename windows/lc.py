import datetime
from functools import partial
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QGroupBox, QGridLayout, QDialog, QVBoxLayout
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
        self.fill_form()

    def fill_form(self):
        self.spec_fill()
        self.unit_fill()

    def spec_fill(self):
        specs = Spec.select()
        for spec in specs:
            btn_spec = SpecBtn(spec)
            self.ui.spec_layout.addWidget(btn_spec)

    def unit_fill(self):
        for unit in Unit.select():
            i = 0
            j = 0
            unit_groupbox = PlaneGroupBox(unit, True, self.ui.podr_groupbox)
            unit_lout = QGridLayout()
            unit_groupbox.setLayout(unit_lout)
            for plane in Plane.select().join(Unit).where(Plane.unit == unit.id):
                i += 1
                if plane.not_deleted:
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
        self.fill_form()

    def fill_form(self):
        self.spec_fill()
        self.unit_fill()

    def spec_fill(self):
        specs = self.lc.spec_for_exec
        for spec in specs:
            spec_btn = SpecBtn(spec)
            self.ui.spec_layout.addWidget(spec_btn)


class ExecLC(QDialog):
    def __init__(self, lc_id, parent=None):
        super().__init__(parent)
        self.lc = ListControl.get_by_id(lc_id)
        self.resize(600, 250)
        self.setWindowTitle('Отметь выполненные самолеты')
        self.globalLayout = QVBoxLayout(self)
        self.setLayout(self.globalLayout)
        self.unitLayout = QHBoxLayout()
        self.globalLayout.addLayout(self.unitLayout)
        self.unit_fill()
        self.btn_connect()
        self.plane_check()

    def btn_connect(self):
        for btn in self.findChildren(PlaneBtn):
            btn.clicked.connect(partial(self.open_exec_spec, btn.plane))

    def open_exec_spec(self, plane):
        spec_window = ExecSpec(plane, self.lc)
        spec_window.exec()

    def unit_fill(self):
        for unit in self.lc.planes_for_exec.keys():
            i, j = 0, 0
            unit_groupbox = PlaneGroupBox(Unit.get(Unit.name == unit))
            unit_lout = QGridLayout()
            unit_groupbox.setLayout(unit_lout)
            planes = self.lc.planes_for_exec[unit]
            for plane in planes:
                i += 1
                btn_plane = PlaneBtn(plane)
                btn_plane.setChecked(True)
                unit_lout.addWidget(btn_plane, j, i)
                if i > 2:
                    j += 1
                    i = 0
            self.unitLayout.addWidget(unit_groupbox)

    def plane_check(self):
        pass
        # planes = self.findChildren(PlaneBtn)
        # specs = self.lc.spec_for_exec
        # for plane_btn in planes:
        #     exec_specs = ListControlExec.select(ListControlExec.spec).where(ListControlExec.id_lk == self.lc.id, ListControlExec.plane == plane_btn.plane.id)
        #     for spec in exec_specs:
        #


class ExecSpec(QDialog):
    def __init__(self, plane: Plane, lc: ListControl, parent=None):
        super().__init__(parent)
        self.lc = lc
        self.plane = plane
        self.resize(300, 100)
        self.setWindowTitle('Отметь выполненные специальности')
        self.globalLayout = QHBoxLayout(self)
        self.setLayout(self.globalLayout)
        self.spec_fill(self.globalLayout, self.lc)

    def spec_fill(self, layout, lc):
        specs = lc.spec_for_exec
        for spec in specs:
            spec_obj = Spec.get(spec)
            btn = SpecBtn(spec_obj, lc)
            btn.clicked.connect(partial(self.switch_spec, self.lc.id, self.plane.id, spec_obj.id))
            spec_check = ListControlExec.get_or_none(
                id_lk=self.lc.id,
                plane=self.plane.id,
                spec=spec_obj.id
            )
            if spec_check is None:
                btn.setChecked(False)
            else:
                btn.setChecked(True)

            layout.addWidget(btn)

    @staticmethod
    def switch_spec(lc_id, plane_id, spec_id):
        res = ListControlExec.get_or_create(
            id_lk=lc_id,
            plane=plane_id,
            spec=spec_id,
            defaults={'date': datetime.date.today()}
        )
        if not res[1]:
            res[0].delete_instance()
