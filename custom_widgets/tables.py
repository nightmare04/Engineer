import datetime

from PyQt6.QtCore import QAbstractTableModel, Qt, QSortFilterProxyModel, QRegularExpression
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import QTableView, QHeaderView, QFormLayout

from custom_widgets.combobox import TypePlaneComboBox
from database.models import *


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


class ListControlProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vypolnen_filter = QRegularExpression()
        self.prosroch_filter = QRegularExpression()
        self.plane_filter = QRegularExpression()

    def filterAcceptsRow(self, sourceRow, sourceParent):
        vypolnen = self.sourceModel().index(sourceRow, 5, sourceParent).data()
        prosrochen = self.sourceModel().index(sourceRow, 3, sourceParent).data()
        plane = self.sourceModel().index(sourceRow, 5, sourceParent).data()

        # Проверяем соответствие каждого значения своим фильтрам
        return self.vypolnen_filter.match(str(vypolnen)).hasMatch() and \
            self.prosroch_filter.match(str(prosrochen)).hasMatch() and \
            self.plane_filter.match(str(plane)).hasMatch()

    def setVypolnenFilter(self, pattern):
        self.vypolnen_filter.setPattern(pattern)
        self.invalidateFilter()

    def setProsrochFilter(self, pattern):
        self.prosroch_filter.setPattern(pattern)
        self.invalidateFilter()

    def setPlaneFilter(self, pattern):
        if pattern == "Все":
            self.plane_filter.setPattern('')
        else:
            self.plane_filter.setPattern(pattern)
        self.invalidateFilter()


class LCTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = ListControlModel(query=ListControl.select())
        self.proxy_model = ListControlProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.setModel(self.proxy_model)
        self.hideColumn(6)
        self.setColumnWidth(5, 200)
        self.verticalHeader().setDefaultSectionSize(75)
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)


class PlaneTableModel(QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dataset = Plane.select().where(Plane.not_delete == True)

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
                return f'{plane.id}'
            elif col == 1:
                return f'{PlaneType.get_by_id(plane.typeId).name}'
            elif col == 2:
                return f'{Unit.get_by_id(plane.typeId).name}'
            elif col == 3:
                return f'{plane.name}'
            elif col == 4:
                return f'{plane.zavNum}'
            elif col == 5:
                return f'{plane.dateVyp.strftime("%d.%m.%Y")}'
            elif col == 6:
                return f'{ZavIzg.get_by_id(plane.vypZav).name}'
            elif col == 7:
                return f'{plane.dateRem.strftime("%d.%m.%Y")}'
            elif col == 8:
                return f'{RemType.get_by_id(plane.remType).name}'
            elif col == 9:
                return f'{RemZav.get_by_id(plane.remZav).name}'
            elif col == 10:
                return f'{self.osob_to_text(plane.osobPlane)}'

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
                    0: "ID",
                    1: "Тип самолета",
                    2: "Подразделение",
                    3: "Бортовой номер",
                    4: "Заводской номер",
                    5: "Дата выпуска",
                    6: "Завод изготовитель",
                    7: "Дата ремонта",
                    8: "Вид ремонта",
                    9: "Ремонтный завод",
                    10: "Особенности самолета"
                }.get(section)
            else:
                return f'{section + 1}'

    def updateData(self):
        self.beginResetModel()
        self._dataset = Plane.select().where(Plane.not_delete == True)
        self.endResetModel()


class PlaneTableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.query = Plane.select().where(Plane.not_delete == True)
        self.model = PlaneTableModel()
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterKeyColumn(5)
        self.setModel(self.proxy_model)
        self.hideColumn(0)
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
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return {
                    0: "ID",
                    1: "Специальность",
                    2: "Система",
                    3: "Агрегат/Блок",
                    4: "Заводской номер",
                    5: "Состояние"
                }.get(section)
            elif orientation == Qt.Orientation.Vertical:
                return section + 1

    def data(self, index, role=...):
        if not index.isValid():
            return
        if role == Qt.ItemDataRole.DisplayRole:
            agregate = self._dataset[index.row()]
            col = index.column()
            if col == 0:
                return agregate.id
            elif col == 1:
                return agregate.agregateId.planeSystem.specId.name
            elif col == 2:
                return agregate.agregateId.planeSystem.name
            elif col == 3:
                return agregate.agregateId.name
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
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return {
                    0: "ID",
                    1: "Тип самолета",
                    2: "Специальность",
                    3: "Система"
                }.get(section)
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
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return {
                    0: "ID",
                    1: "Тип самолета",
                    2: "Особенность"
                }.get(section)
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
                return osob.typeId.name
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


class ZavodIzgTableModel(QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dataset = ZavIzg.select().where(ZavIzg.not_delete == True)

    def rowCount(self, parent=...):
        return len(self._dataset)

    def columnCount(self, parent=...):
        return 2

    def headerData(self, section, orientation, role=...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return {
                    0: "ID",
                    1: "Завод изготовитель"
                }.get(section)
            elif orientation == Qt.Orientation.Vertical:
                return section + 1

    def data(self, index, role=...):
        if not index.isValid():
            return
        if role == Qt.ItemDataRole.DisplayRole:
            zavod_izg = self._dataset[index.row()]
            col = index.column()
            if col == 0:
                return zavod_izg.id
            elif col == 1:
                return zavod_izg.name

    def updateData(self):
        self.beginResetModel()
        self._dataset = ZavIzg.select().where(ZavIzg.not_delete == True)
        self.endResetModel()


class ZavodIzgTableView(QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = ZavodIzgTableModel()
        self.setModel(self.model)
        self.hideColumn(0)
        self.verticalHeader().setDefaultSectionSize(30)


class RemTypeTableModel(QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dataset = RemType.select().where(RemType.not_delete == True)

    def rowCount(self, parent=...):
        return len(self._dataset)

    def columnCount(self, parent=...):
        return 3

    def headerData(self, section, orientation, role=...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return {
                    0: "ID",
                    1: "Тип самолета",
                    2: "Тип ремонта"
                }.get(section)
            elif orientation == Qt.Orientation.Vertical:
                return section + 1

    def data(self, index, role=...):
        if not index.isValid():
            return
        if role == Qt.ItemDataRole.DisplayRole:
            rem_type = self._dataset[index.row()]
            col = index.column()
            if col == 0:
                return rem_type.id
            elif col == 1:
                return rem_type.typeId.name
            elif col == 2:
                return rem_type.name

    def updateData(self):
        self.beginResetModel()
        self._dataset = RemType.select().where(RemType.not_delete == True)
        self.endResetModel()


class RemTypeTableView(QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = RemTypeTableModel()
        self.setModel(self.model)
        self.hideColumn(0)
        self.verticalHeader().setDefaultSectionSize(30)


class PlaneSystemTableModel(QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dataset = PlaneSystem.select().where(PlaneSystem.not_delete == True)

    def rowCount(self, parent=...):
        return len(self._dataset)

    def columnCount(self, parent=...):
        return 4

    def headerData(self, section, orientation, role=...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return {
                    0: "ID",
                    1: "Тип самолета",
                    2: "Специальность",
                    3: "Система"
                }.get(section)
            elif orientation == Qt.Orientation.Vertical:
                return section + 1

    def data(self, index, role=...):
        if not index.isValid():
            return
        if role == Qt.ItemDataRole.DisplayRole:
            plane_system = self._dataset[index.row()]
            col = index.column()
            if col == 0:
                return plane_system.id
            elif col == 1:
                return plane_system.typeId.name
            elif col == 2:
                return plane_system.specId.name
            elif col == 3:
                return plane_system.name

    def updateData(self):
        self.beginResetModel()
        self._dataset = PlaneSystem.select().where(PlaneSystem.not_delete == True)
        self.endResetModel()


class PlaneSystemProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.type_filter = QRegularExpression()
        self.spec_filter = QRegularExpression()

    def filterAcceptsRow(self, sourceRow, sourceParent):

        type_name = self.sourceModel().index(sourceRow, 1, sourceParent).data()
        spec_name = self.sourceModel().index(sourceRow, 2, sourceParent).data()

        # Проверяем соответствие каждого значения своим фильтрам
        return self.type_filter.match(str(type_name)).hasMatch() and \
            self.spec_filter.match(str(spec_name)).hasMatch()

    def setTypeFilter(self, pattern):
        self.type_filter.setPattern(pattern)
        self.invalidateFilter()

    def setSpecFilter(self, pattern):
        self.spec_filter.setPattern(pattern)
        self.invalidateFilter()


class PlaneSystemTableView(QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = PlaneSystemTableModel()
        self.proxy_model = PlaneSystemProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.setModel(self.proxy_model)
        self.proxy_model.setFilterKeyColumn(1)

        self.hideColumn(0)
        self.verticalHeader().setDefaultSectionSize(30)


class AgregateStateTableModel(QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dataset = AgregateState.select().where(AgregateState.not_delete == True)

    def rowCount(self, parent=...):
        return len(self._dataset)

    def columnCount(self, parent=...):
        return 2

    def headerData(self, section, orientation, role=...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return {
                    0: "ID",
                    1: "Состояние"
                }.get(section)
            elif orientation == Qt.Orientation.Vertical:
                return section + 1

    def data(self, index, role=...):
        if not index.isValid():
            return
        if role == Qt.ItemDataRole.DisplayRole:
            agregate_state = self._dataset[index.row()]
            col = index.column()
            if col == 0:
                return agregate_state.id
            elif col == 1:
                return agregate_state.name

    def updateData(self):
        self.beginResetModel()
        self._dataset = AgregateState.select().where(AgregateState.not_delete == True)
        self.endResetModel()


class AgregateStateTableView(QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = AgregateStateTableModel()
        self.setModel(self.model)
        self.hideColumn(0)
        self.verticalHeader().setDefaultSectionSize(30)
