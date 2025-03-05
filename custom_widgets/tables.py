from tkinter.tix import ResizeHandle

from PyQt6.QtWidgets import QTableView, QHeaderView
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, QSortFilterProxyModel
from PyQt6.QtGui import QBrush, QColor
from peewee import reraise


from database.models import *
import datetime


class AllTableModel(QAbstractTableModel):
    def __init__(self, basemodel, header, query, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = query
        self.basemodel = basemodel
        self._dataset = basemodel.select().where(basemodel.not_delete == True)
        self.header = header

    def columnCount(self, parent=...):
        return 2

    def rowCount(self, parent=...):
        return len(self._dataset)

    def data(self, index, role=...):
        if not index.isValid():
            return
        if role == Qt.ItemDataRole.DisplayRole:
            data = self._dataset[index.row()]
            col = index.column()
            if col == 0:
                return f'{data.id}'
            elif col == 1:
                return f'{data.name}'

    def headerData(self, section, orientation, role=...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.header[section]
            elif orientation == Qt.Orientation.Vertical:
                return f'{section + 1}'

    def updateData(self, query=None):
        self.beginResetModel()
        self._dataset = self.basemodel.select().where(self.basemodel.not_delete == True)
        self.endResetModel()


class AllTableView(QTableView):
    def __init__(self, header, basemodel, parent=None):
        super().__init__(parent)
        self.query = basemodel.select().where(basemodel.not_delete == True)
        self.model = AllTableModel(basemodel=basemodel, header=header, query=self.query)
        self.setModel(self.model)
        self.hideColumn(0)
        self.verticalHeader().setDefaultSectionSize(30)


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
        res = "Не выполнено: "
        for plane_id in planes_incomplete:
            plane = Plane.get_by_id(plane_id)
            res += f'{plane.name}, '
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
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)


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
                return f'{PlaneType.get_by_id(plane.typeId).name}'
            elif col == 1:
                return f'{Unit.get_by_id(plane.plane_type).name}'
            elif col == 2:
                return f'{plane.name}'
            elif col == 3:
                return f'{plane.zavNum}'
            elif col == 4:
                return f'{plane.dateVyp.strftime("%d.%m.%Y")}'
            elif col == 5:
                return f'{VypZav.get_by_id(plane.vypZav).name}'
            elif col == 6:
                return f'{plane.dateRem.strftime("%d.%m.%Y")}'
            elif col == 7:
                return f'{RemType.get_by_id(plane.remType).name}'
            elif col == 8:
                return f'{RemZav.get_by_id(plane.remZav).name}'
            elif col == 9:
                return f'{self.osob_to_text(plane.osobPlane)}'
            elif col == 10:
                return f'{plane.id}'

    @staticmethod
    def osob_to_text(osobs):
        res = ''
        for osob in osobs:
            res += f"{OsobPlane.get_by_id(osob).name}, "
        res = res[:-2]
        return res

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
    def __init__(self, header, basemodel, parent=None):
        super().__init__(parent)
        self.head = header
        self.instance = basemodel
        self.query = Plane.select().where(Plane.not_delete == True)
        self.model = PlaneTableModel(query=self.query)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(5)
        self.setModel(self.proxy_model)
        self.hideColumn(10)
        # self.setColumnWidth(5, 200)
        self.verticalHeader().setDefaultSectionSize(90)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeMode.Stretch)


class PlaneTypeTableModel(AllTableModel):
    def __init__(self, query, *args, **kwargs):
        super().__init__(query, *args, **kwargs)

    def headerData(self, section, orientation, role=...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return {
                    0: "Тип самолета",
                    1: "ID"
                }.get(section)
            elif orientation == Qt.Orientation.Vertical:
                return f'{section + 1}'


class IspravnostPlaneTableModel(QAbstractTableModel):
    def __init__(self, plane: Plane, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plane = plane
        self._dataset = AgregateOnPlane.select().where(AgregateOnPlane.planeId == self.plane.id)

    def rowCount(self, parent=...):
        return len(AgregateOnPlane.select().where(AgregateOnPlane.planeId == self.plane.id))

    def columnCount(self, parent=...):
        return 6

    def headerData(self, section, orientation, role = ...):
        if orientation == Qt.Orientation.Horizontal:
            return ["ID", "Специальность", "Система", "Агрегат/Блок", "Заводской номер", "Состояние"]
        elif orientation == Qt.Orientation.Vertical:
            return section + 1

    def data(self, index, role = ...):
        if not index.isValid():
            return
        if role == Qt.ItemDataRole.DisplayRole:
            agregate = self._dataset[index.row()]
            col = index.column()
            if col == 0:
                return agregate.id
            elif col == 1:
                return agregate.planeAgregate.planeSystem.specId.name
            elif col == 2:
                return agregate.planeAgregate.planeSystem.name
            elif col == 3:
                return agregate.planeAgregate.name
            elif col == 4:
                return agregate.zavNum
            elif col == 5:
                return agregate.state.name

    def updateData(self):
        self.beginResetModel()
        self._dataset = AgregateOnPlane.select().where(AgregateOnPlane.planeId == self.plane.id)
        self.endResetModel()


class IspravnostPlaneTableView(QTableView):
    def __init__(self, plane, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = IspravnostPlaneTableModel(plane)
        self.setModel(self.model)
        self.hideColumn(0)
        self.verticalHeader().setDefaultSectionSize(30)


class SystemPlaneTableModel(QAbstractTableModel):
    def __init__(self, plane: Plane, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plane = plane
        self._dataset = PlaneSystem.select().where(PlaneSystem.not_delete == True)

    def rowCount(self, parent=...):
        return len(self._dataset)

    def columnCount(self, parent=...):
        return 4

    def headerData(self, section, orientation, role=...):
        if orientation == Qt.Orientation.Horizontal:
            return ["ID", "Тип самолета", "Специальность", "Система"]
        elif orientation == Qt.Orientation.Vertical:
            return section + 1

    def data(self, index, role=...):
        if not index.isValid():
            return
        if role == Qt.ItemDataRole.DisplayRole:
            system = self._dataset[index.row()]
            col = index.column()
            if col == 0:
                return system.id
            elif col == 1:
                return system.typeId.name
            elif col == 2:
                return system.specId.name
            elif col == 3:
                return system.name

    def updateData(self):
        self.beginResetModel()
        self._dataset = PlaneSystem.select().where(PlaneSystem.not_delete == True)
        self.endResetModel()


class SystemPlaneTableView(QTableView):
    def __init__(self, plane, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = IspravnostPlaneTableModel(plane)
        self.setModel(self.model)
        self.hideColumn(0)
        self.verticalHeader().setDefaultSectionSize(30)


class OsobPlaneTableModel(QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dataset = OsobPlane.select().where(OsobPlane.not_delete == True)

    def rowCount(self, parent=...):
        return len(self._dataset)

    def columnCount(self, parent=...):
        return 3

    def headerData(self, section, orientation, role=...):
        if orientation == Qt.Orientation.Horizontal:
            return ["ID", "Тип самолета", "Особенность"]
        elif orientation == Qt.Orientation.Vertical:
            return section + 1

    def data(self, index, role=...):
        if not index.isValid():
            return
        if role == Qt.ItemDataRole.DisplayRole:
            osob = self._dataset[index.row()]
            col = index.column()
            if col == 0:
                return osob.id
            elif col == 1:
                return osob.planeType.name
            elif col == 2:
                return osob.name

    def updateData(self):
        self.beginResetModel()
        self._dataset = OsobPlane.select().where(OsobPlane.not_delete == True)
        self.endResetModel()


class OsobPlaneTableView(QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = OsobPlaneTableModel()
        self.setModel(self.model)
        self.hideColumn(0)
        self.verticalHeader().setDefaultSectionSize(30)

