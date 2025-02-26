from PyQt6.QtWidgets import QTableView
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, QSortFilterProxyModel
from PyQt6.QtGui import QBrush, QColor
from peewee import reraise

from database.models import ListControl, ListControlExec, Plane, PlaneType, Unit, OsobPlane
import datetime


class MyTableModel(QAbstractTableModel):
    def __init__(self, query, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dataset = query

    def columnCount(self, parent=...):
        return 1

    def rowCount(self, parent=...):
        return len(self._dataset)

    def data(self, index, role=...):
        if not index.isValid():
            return
        if role == Qt.ItemDataRole.DisplayRole:
            data = self._dataset[index.row()]
            col = index.column()
            if col == 0:
                return f'{data.name}'
            elif col == 1:
                return f'{data.id}'

    def updateData(self, query):
        self.beginResetModel()
        self._dataset = query
        self.endResetModel()


class ListControlModel(QAbstractTableModel):
    def __init__(self, query, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dataset = query

    @staticmethod
    def get_not_complete(lc: ListControl) -> str:
        planes_incomplete = []
        for unit in lc.planes["to_exec"].keys():
            plane_ex = True
            for plane_id in lc.planes["to_exec"][unit]:
                for spec in lc.specs["to_exec"]:
                    if ListControlExec.get_or_none(ListControlExec.planeId == plane_id,
                                                   ListControlExec.lcId == lc.id,
                                                   ListControlExec.specId == spec) is None:
                        plane_ex = False
                if not plane_ex:
                    planes_incomplete.append(plane_id)
        if len(planes_incomplete) == 0:
            return "Все выполнено"
        res = "Не выполнено на ВС: "
        for plane_id in planes_incomplete:
            res += f'{Plane.get_by_id(plane_id).bortNum}, '
        res = res[:-2]
        return res

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
                return f'{lc.lcNumber}'
            elif col == 1:
                return f'{lc.tlg}'
            elif col == 2:
                return f'{lc.tlgDate.strftime("%d.%m.%Y")}'
            elif col == 3:
                if not self.get_not_complete(lc) == "Все выполнено":
                    return f'{self.get_delta(lc.tlgDeadline)}'
                else:
                    return ""
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
                count = lc.tlgDeadline - datetime.date.today()
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
        self.model = ListControlModel(query=ListControl.select())
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(5)
        self.setModel(self.proxy_model)
        self.hideColumn(6)
        self.setColumnWidth(5, 200)
        self.verticalHeader().setDefaultSectionSize(75)


class PlaneTableModel(QAbstractTableModel):
    def __init__(self, query, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dataset = query

    def columnCount(self, parent=...):
        return 11

    def rowCount(self, parent=...):
        return len(self._dataset)

    def data(self, index, role=...):
        if not index.isValid():
            return
        if role == Qt.ItemDataRole.DisplayRole:
            plane = self._dataset[index.row()]
            col = index.column()
            if col == 0:
                return f'{plane.planeType}'
            elif col == 1:
                return f'{plane.unit}'
            elif col == 2:
                return f'{plane.bortNum}'
            elif col == 3:
                return f'{plane.zavNum}'
            elif col == 4:
                return f'{plane.dateVyp}'
            elif col == 5:
                return f'{plane.vypZav}'
            elif col == 6:
                return f'{plane.dateRem}'
            elif col == 7:
                return f'{plane.remType}'
            elif col == 8:
                return f'{plane.remZav}'
            elif col == 9:
                return f'{plane.osobPlane}'
            elif col == 10:
                return f'{plane.id}'

    def headerData(self, section, orientation, role=...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return {
                    0: "Тип самолета",
                    1: "Подразделение",
                    2: "Бортовой номер",
                    3: "Заводской номер",
                    4: "Дата выпуска",
                    5: "Завод изготовитель",
                    6: "Дата ремонта",
                    7: "Вид ремонта",
                    8: "Ремонтный завод",
                    9: "Особенности самолета",
                    10: "ID"
                }.get(section)
            else:
                return f'{section + 1}'

    def updateData(self, query):
        self.beginResetModel()
        self._dataset = query
        self.endResetModel()


class PlaneTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.query = Plane.select().where(Plane.not_delete == True)
        self.model = PlaneTableModel(query=self.query)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(5)
        self.setModel(self.proxy_model)
        self.hideColumn(10)
        # self.setColumnWidth(5, 200)
        self.verticalHeader().setDefaultSectionSize(30)


class PlaneTypeTableModel(MyTableModel):
    def __init__(self, query, *args, **kwargs):
        super().__init__(query, *args, **kwargs)

    def headerData(self, section, orientation, role=...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return {
                    0: "Тип самолета",
                    1: "ID"
                }.get(section)
            else:
                return f'{section + 1}'


class PlaneTypeTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.query = PlaneType.select().where(PlaneType.not_delete == True)
        self.model = PlaneTypeTableModel(query=self.query)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.setModel(self.proxy_model)
        self.hideColumn(1)
        self.verticalHeader().setDefaultSectionSize(30)


class UnitTableModel(MyTableModel):
    def __init__(self, query, *args, **kwargs):
        super().__init__(query, *args, **kwargs)

    def headerData(self, section, orientation, role=...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return {
                    0: "Подразделение",
                    1: "ID"
                }.get(section)
            else:
                return f'{section + 1}'


class UnitTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.query = Unit.select().where(Unit.not_delete == True)
        self.model = UnitTableModel(query=self.query)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.setModel(self.proxy_model)
        self.hideColumn(1)
        self.verticalHeader().setDefaultSectionSize(30)


class OsobTableModel(MyTableModel):
    def __init__(self, query, *args, **kwargs):
        super().__init__(query, *args, **kwargs)

    def columnCount(self, parent=...):
        return 3

    def data(self, index, role=...):
        if not index.isValid():
            return
        if role == Qt.ItemDataRole.DisplayRole:
            data = self._dataset[index.row()]
            col = index.column()
            if col == 0:
                return f'{data.name}'
            elif col == 1:
                return f'{data.planeType.name}'
            elif col == 2:
                return f'{data.id}'

    def headerData(self, section, orientation, role=...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return {
                    0: "Особенность",
                    1: "Тип самолета",
                    2: "ID"
                }.get(section)
            else:
                return f'{section + 1}'


class OsobTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.query = OsobPlane.select().where(OsobPlane.not_delete == True)
        self.model = OsobTableModel(query=self.query)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.setModel(self.proxy_model)
        self.hideColumn(2)
        self.verticalHeader().setDefaultSectionSize(30)