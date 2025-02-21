import datetime

from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt6.QtWidgets import QTableView
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QColor, QBrush
from PyQt6.uic.Compiler.qtproxies import QtGui

from database.models import *
from windows.lc import ExecLC
from custom_widgets.groupboxs import PlaneGroupBox
from custom_widgets.buttons import PlaneBtn, SpecBtn

class ListControlModel(QAbstractTableModel):
    def __init__(self, select, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = select

    @staticmethod
    def get_delta(deadline):
        count = deadline - datetime.date.today()
        if count.days < 0:
            return "Просрочен на :" + str(count.days) + " дней"
        else:
            return "Осталось " + str(count.days) + " дней"

    def get_not_complete(self, lc: ListControl) -> str:
        planes_incomplete = []
        for unit in lc.planes_for_exec.keys():
            plane_ex = True
            for plane_id in lc.planes_for_exec[unit]:
                for spec in lc.spec_for_exec:
                    if ListControlExec.get_or_none(ListControlExec.plane_id == plane_id,
                                                   ListControlExec.lc_id == lc.id,
                                                   ListControlExec.spec_id == spec) is None:
                        plane_ex = False
                if not plane_ex:
                    planes_incomplete.append(plane_id)
        if len(planes_incomplete)==0:
            return "Все выполнено"
        res = "Не выполнено на ВС: "
        for plane_id in planes_incomplete:
            res += f'{Plane.get_by_id(plane_id).bort_num}, '
        res = res[:-2]
        return res

    def rowCount(self, *args, **kwargs) -> int:
        return len(self.query)

    def columnCount(self, *args, **kwargs) -> int:
        return 7

    def data(self, index: QModelIndex, role: Qt.ItemDataRole):
        if not index.isValid():
            return
        if role == Qt.ItemDataRole.DisplayRole:
            lc = self.query[index.row()]
            col = index.column()
            if col == 0:
                return f'{lc.lc_number}'
            elif col == 1:
                return f'{lc.tlg}'
            elif col == 2:
                return f'{lc.tlg_date}'
            elif col == 3:
                return f'{self.get_delta(lc.tlg_deadline)}'
            elif col == 4:
                return f'{lc.description}'
            elif col == 5:
                return self.get_not_complete(lc)
            elif col == 6:
                return lc.id

        if role == Qt.ItemDataRole.BackgroundRole:
            lc = self.query[index.row()]
            col = index.column()
            if col == 3:
                count = lc.tlg_deadline - datetime.date.today()
                if count.days <= 0:
                    return QBrush(QColor('red'))

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return {
                    0: "Номер ЛК",
                    1: "ТЛГ/Указание",
                    2: "Дата ТЛГ",
                    3: "Осталось дней",
                    4: "Описание",
                    5: "Не выполнено",
                    6: "ID"
                }.get(section)
            else:
                return f'{section+1}'




def fill_lc(tableview: QTableView):
    model = ListControlModel(select=ListControl.select())
    tableview.setModel(model)
    tableview.hideColumn(6)
    tableview.clicked.connect(lambda index: exec_lc(index.siblingAtColumn(6).data()))


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
            if plane.isChecked() and plane.plane_id.not_deleted:
                res_plane.append(plane.plane_id.id)
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

