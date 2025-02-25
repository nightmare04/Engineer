from PyQt6.QtWidgets import QTableView
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, QSortFilterProxyModel
from PyQt6.QtGui import QBrush, QColor
from database.models import ListControl, ListControlExec, Plane
import datetime


class ListControlModel(QAbstractTableModel):
    def __init__(self, select, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dataset = select

    @staticmethod
    def plural_days(n):
        days = ['день', 'дня', 'дней']

        if n % 10 == 1 and n % 100 != 11:
            p = 0
        elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
            p = 1
        else:
            p = 2

        return str(n) + ' ' + days[p]

    def get_delta(self, deadline):
        count = deadline - datetime.date.today()
        if count.days < 0:
            return "Просрочен на :" + self.plural_days(abs(count.days))
        else:
            return "Осталось " + self.plural_days(count.days)

    @staticmethod
    def get_not_complete(lc: ListControl) -> str:
        planes_incomplete = []
        for unit in lc.planes["to_exec"].keys():
            plane_ex = True
            for plane_id in lc.planes["to_exec"][unit]:
                for spec in lc.specs["to_exec"]:
                    if ListControlExec.get_or_none(ListControlExec.plane_id == plane_id,
                                                   ListControlExec.lc_id == lc.id,
                                                   ListControlExec.spec_id == spec) is None:
                        plane_ex = False
                if not plane_ex:
                    planes_incomplete.append(plane_id)
        if len(planes_incomplete) == 0:
            return "Все выполнено"
        res = "Не выполнено на ВС: "
        for plane_id in planes_incomplete:
            res += f'{Plane.get_by_id(plane_id).bort_num}, '
        res = res[:-2]
        return res

    def rowCount(self, *args, **kwargs) -> int:
        return len(self._dataset)

    def columnCount(self, *args, **kwargs) -> int:
        return 7

    def data(self, index, role=...):
        if not index.isValid():
            return
        if role == Qt.ItemDataRole.DisplayRole:
            lc = self._dataset[index.row()]
            col = index.column()
            if col == 0:
                return f'{lc.lc_number}'
            elif col == 1:
                return f'{lc.tlg}'
            elif col == 2:
                return f'{lc.tlg_date.strftime("%d.%m.%Y")}'
            elif col == 3:
                if not self.get_not_complete(lc) == "Все выполнено":
                    return f'{self.get_delta(lc.tlg_deadline)}'
                else:
                    return "Все выполнено"
            elif col == 4:
                return f'{lc.description}'
            elif col == 5:
                return self.get_not_complete(lc)
            elif col == 6:
                return lc.id

        if role == Qt.ItemDataRole.BackgroundRole:
            lc = self._dataset[index.row()]
            col = index.column()
            if self.get_not_complete(lc) == "Все выполнено":
                return QBrush(QColor('green'))
            if col == 3:
                count = lc.tlg_deadline - datetime.date.today()
                if count.days <= 0 and not self.get_not_complete(lc) == "Все выполнено":
                    return QBrush(QColor('red'))


    def headerData(self, section, orientation, role=...):
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

    def updateData(self, dataset):
        self.beginResetModel()
        self._dataset = dataset
        self.endResetModel()


class LCTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = ListControlModel(select=ListControl.select())
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(5)
        self.setModel(self.proxy_model)
        self.hideColumn(6)
        self.setColumnWidth(5, 200)
        self.verticalHeader().setDefaultSectionSize(75)
