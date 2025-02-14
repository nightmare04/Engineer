import datetime

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QGroupBox

from custom_widgets import PlaneGroupBox, PlaneBtn, SpecBtn
from database.database import *
from ui import Ui_MainWindow
import windows.lc
from windows.lc import EditLC, AddLC, ExecLC


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        create_tables()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("ИАС")
        self.ui.stackedWidget.setCurrentWidget(self.ui.lk_page)
        self.fill_lk()
        self.ui.btn_add_lk.clicked.connect(self.add_lc_window)
        self.ui.btn_pki.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.pki_page))
        self.ui.btn_lk.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.lk_page))
        self.ui.btn_ispr.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.ispr_page))
        self.ui.btn_rekl.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.rekl_page))
        self.ui.type_plane_action.triggered.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.rekl_page))

    def fill_lk(self):
        model = QStandardItemModel(self)
        model.setHorizontalHeaderLabels(["", "№ ЛК", "ТЛГ", "Дата ТЛГ", "Срок до", "Описание", "Выполнено"])
        lcs = ListControl.select()
        for lc in lcs:
            id_lc = QStandardItem(str(lc.id))
            tlg = QStandardItem(str(lc.tlg))
            numlc = QStandardItem(str(lc.lc_number))
            tlg_date = QStandardItem(str(lc.tlg_date))
            deadline = lc.tlg_deadline - datetime.date.today()
            tlg_deadline = QStandardItem(self.delta_to_text(deadline),)
            if deadline.days < 0:
                tlg_deadline.setBackground(QtGui.QColor('red'))
            tlg_desc = QStandardItem(lc.description)
            tlg_desc.setEditable(False)
            tlg_cf = QStandardItem(lc.complete_flag)
            model.appendRow([id_lc, numlc, tlg, tlg_date, tlg_deadline, tlg_desc, tlg_cf])
        self.ui.tableView.setModel(model)
        self.ui.tableView.hideColumn(0)
        self.ui.tableView.clicked.connect(lambda index: self.exec_lc(index.siblingAtColumn(0).data()))

    @staticmethod
    def delta_to_text(timedelta: datetime.timedelta) -> str:
        if timedelta.days < 0:
            return "Просрочен на :" + str(timedelta.days) + " дней"
        else:
            return "Осталось " + str(timedelta.days) + " дней"

    @staticmethod
    def exec_lc(lc_id):
        exlcw = ExecLC(lc_id)
        exlcw.exec()
        self.fill_lk()

    def load_lc(self, lc_id):
        lcw = EditLC(lc_id)
        if lcw.exec():
            self.save_lc(lcw, lcw.lc)
        self.fill_lk()

    def add_lc_window(self):
        lcw = AddLC()
        if lcw.exec():
            self.add_lc(lcw)
        self.fill_lk()

    def add_lc(self, dialog):
        lc = ListControl()
        lc.tlg = dialog.ui.tlgEdit.text()
        lc.tlg_date = dialog.ui.tlgDateEdit.date().toPyDate()
        lc.lc_number = dialog.ui.lcEdit.text()
        lc.planes_for_exec = self.dump_plane(dialog)
        lc.spec_for_exec = self.dump_spec(dialog)
        lc.tlg_deadline = dialog.ui.tlgDeadlineEdit.date().toPyDate()
        lc.description = dialog.ui.textEdit.toPlainText()
        lc.save()

    def save_lc(self, dialog, lc: ListControl):
        lc.tlg = dialog.ui.tlgEdit.text()
        lc.tlg_date = dialog.ui.tlgDateEdit.date().toPyDate()
        lc.lc_number = dialog.ui.lcEdit.text()
        lc.planes_for_exec = self.dump_plane(dialog)
        lc.spec_for_exec = self.dump_spec(dialog)
        lc.tlg_deadline = dialog.ui.tlgDeadlineEdit.date().toPyDate()
        lc.description = dialog.ui.textEdit.toPlainText()
        lc.update()

    @staticmethod
    def dump_spec(dialog):
        res = []
        specs = dialog.ui.spec_groupbox.findChildren(SpecBtn)
        for spec in specs:
            if spec.isChecked():
                res.append(spec.spec_name)
        return res

    @staticmethod
    def dump_plane(dialog):
        res = {}
        units_gb = dialog.ui.podr_groupbox.findChildren(PlaneGroupBox)
        for unit in units_gb:
            res_plane = []
            planes = unit.findChildren(PlaneBtn)
            for plane in planes:
                if plane.isChecked():
                    res_plane.append(plane.plane.bort_num)
            if res_plane:
                res.update({unit.title(): res_plane})
        return res
