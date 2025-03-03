import datetime
from functools import partial


from PyQt6.QtWidgets import QTableView, QStyledItemDelegate, QPushButton
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QColor, QBrush
from custom_widgets.buttons import PlaneBtn, SpecBtn
from database.models import *
from custom_widgets.groupboxs import PlaneGroupBox


def add_lc(w, lc_obj=None):
    if lc_obj is None:
        lc = ListControl()
    else:
        lc = lc_obj
    lc.tlg = w.tlgEdit.text()
    lc.tlgDate = w.tlgDateEdit.date().toPyDate()
    lc.lcNumber = w.lcNumber.text()
    lc.planes = dump_plane(w)
    lc.specs = dump_spec(w)
    lc.tlgDeadline = w.ui.tlgDeadlineEdit.date().toPyDate()
    lc.description = w.ui.textEdit.toPlainText()
    lc.save()


def update_lc(w, lc: ListControl):
    lc.tlg = w.ui.tlgEdit.text()
    lc.tlgDate = w.ui.tlgDateEdit.date().toPyDate()
    lc.lcNumber = w.ui.lcEdit.text()
    lc.planes = self.dump_plane(w)
    lc.spec = self.dump_spec(w)
    lc.tlgDeadline = w.ui.tlgDeadlineEdit.date().toPyDate()
    lc.description = w.ui.textEdit.toPlainText()
    lc.update()


def dump_spec(w):
    spec_on_create = []
    spec_to_exec = []
    specs_btns = w.ui.spec_groupbox.findChildren(SpecBtn)
    for spec_btn in specs_btns:
        spec_on_create.append(spec_btn.spec.id)
        if spec_btn.isChecked():
            spec_to_exec.append(spec_btn.spec.id)
    res = {}
    res.update({"on_create": spec_on_create})
    res.update({"to_exec": spec_to_exec})
    return res


def dump_plane(w):
    plane_to_exec = {}
    plane_on_create = {}
    res = {}
    units_gb = w.ui.podr_groupbox.findChildren(PlaneGroupBox)
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