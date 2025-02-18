import datetime

from PyQt6.QtWidgets import QTableView
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QColor
from database.models import *
from windows.lc import ExecLC
from custom_widgets.groupboxs import PlaneGroupBox
from custom_widgets.buttons import PlaneBtn, SpecBtn


def fill_lc(tableview: QTableView):
    model = QStandardItemModel()
    model.setHorizontalHeaderLabels(["", "№ ЛК", "ТЛГ", "Дата ТЛГ", "Срок до", "Описание", "Выполнено"])
    lcs = ListControl.select()
    for lc in lcs:
        id_lc = QStandardItem(str(lc.id))
        tlg = QStandardItem(str(lc.tlg))
        numlc = QStandardItem(str(lc.lc_number))
        tlg_date = QStandardItem(str(lc.tlg_date))
        deadline = lc.tlg_deadline - datetime.date.today()
        tlg_deadline = QStandardItem(delta_to_text(deadline), )
        if deadline.days < 0:
            tlg_deadline.setBackground(QColor('red'))
        tlg_desc = QStandardItem(lc.description)
        tlg_desc.setEditable(False)
        tlg_cf = QStandardItem(lc.complete_flag)
        model.appendRow([id_lc, numlc, tlg, tlg_date, tlg_deadline, tlg_desc, tlg_cf])
    tableview.setModel(model)
    tableview.hideColumn(0)
    tableview.clicked.connect(lambda index: exec_lc(index.siblingAtColumn(0).data()))


def add_lc(w):
    lc = ListControl()
    lc.tlg = w.ui.tlgEdit.text()
    lc.tlg_date = w.ui.tlgDateEdit.date().toPyDate()
    lc.lc_number = w.ui.lcEdit.text()
    lc.planes_for_exec = dump_plane(w)
    lc.spec_for_exec = dump_spec(w)
    lc.tlg_deadline = w.ui.tlgDeadlineEdit.date().toPyDate()
    lc.description = w.ui.textEdit.toPlainText()
    lc.save()


def update_lc(w, lc: ListControl):
    lc.tlg = w.ui.tlgEdit.text()
    lc.tlg_date = w.ui.tlgDateEdit.date().toPyDate()
    lc.lc_number = w.ui.lcEdit.text()
    lc.planes_for_exec = self.dump_plane(w)
    lc.spec_for_exec = self.dump_spec(w)
    lc.tlg_deadline = w.ui.tlgDeadlineEdit.date().toPyDate()
    lc.description = w.ui.textEdit.toPlainText()
    lc.update()


def dump_spec(w):
    res = []
    specs_btns = w.ui.spec_groupbox.findChildren(SpecBtn)
    for spec_btn in specs_btns:
        if spec_btn.isChecked():
            res.append(spec_btn.spec.id)
    return res


def dump_plane(w):
    res = {}
    units_gb = w.ui.podr_groupbox.findChildren(PlaneGroupBox)
    for unit_gb in units_gb:
        res_plane = []
        planes = unit_gb.findChildren(PlaneBtn)
        for plane in planes:
            if plane.isChecked():
                res_plane.append(plane.plane.id)
        if res_plane:
            res.update({unit_gb.unit.id: res_plane})
    return res


def delta_to_text(timedelta: datetime.timedelta) -> str:
    if timedelta.days < 0:
        return "Просрочен на :" + str(timedelta.days) + " дней"
    else:
        return "Осталось " + str(timedelta.days) + " дней"


def exec_lc(lc_id):
    exlcw = ExecLC(lc_id)
    exlcw.exec()


def load_lc(lc_id):
    lcw = EditLC(lc_id)
    if lcw.exec():
        update_lc(lcw, lcw.lc)

