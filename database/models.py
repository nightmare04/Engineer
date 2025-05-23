from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase, JSONField

# db = SqliteExtDatabase('./database/pw.db', pragmas={'foreign_keys': 1})
db = SqliteExtDatabase('./database/pw.db', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    id = PrimaryKeyField(null=False, unique=True)

    class Meta:
        database = db


class ListControl(BaseModel):
    tlg = CharField(max_length=100, null=False)
    tlgDate = DateField()
    tlgDeadline = DateField()
    description = TextField(null=True)
    lcNumber = CharField(max_length=10, null=True)
    answer = CharField(max_length=100, null=True)
    answerDate = DateField(null=True)
    specs = JSONField()
    planes = JSONField()

    class Meta:
        db_table = 'list_controls'


class PlaneType(BaseModel):
    name = CharField(max_length=30, null=False)
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'plane_types'


class Unit(BaseModel):
    name = CharField(max_length=100, null=False)
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'units'


class RemZav(BaseModel):
    name = CharField(max_length=30, null=False)
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'rem_zav'


class ZavIzg(BaseModel):
    name = CharField(max_length=30, null=False)
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'vyp_zav'


class Plane(BaseModel):
    typeId = ForeignKeyField(PlaneType, backref='planes')
    zavNum = CharField(max_length=30, null=False)
    name = CharField(max_length=10, null=False)
    dateVyp = DateField()
    dateRem = DateField()
    remType = CharField(max_length=30, null=False)
    remZav = ForeignKeyField(RemZav)
    vypZav = ForeignKeyField(ZavIzg)
    osobPlane = JSONField()
    unit = ForeignKeyField(Unit, backref='planes')
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'planes'


class RemType(BaseModel):
    name = CharField(max_length=30, null=False)
    typeId = ForeignKeyField(PlaneType)
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'rem_type'


class OsobPlane(BaseModel):
    typeId = ForeignKeyField(PlaneType)
    name = CharField(max_length=30, null=False)
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'osob_plane'


class Spec(BaseModel):
    name = CharField(max_length=100, null=False)
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'specs'


class ListControlExec(BaseModel):
    lcId = ForeignKeyField(ListControl, backref='lcexec', on_delete='cascade')
    planeId = ForeignKeyField(Plane, backref='lcexec')
    specId = ForeignKeyField(Spec, backref='lcexec')
    date = DateField()

    class Meta:
        db_table = 'list_control_execs'


class PlaneSystem(BaseModel):
    typeId = ForeignKeyField(PlaneType)
    specId = ForeignKeyField(Spec, backref='lcexec')
    name = CharField(max_length=100, null=False)
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'plane_systems'


class AgregateState(BaseModel):
    name = CharField(max_length=100, null=False)
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'agregate_states'


class AgregateName(BaseModel):
    typeId = ForeignKeyField(PlaneType)
    specId = ForeignKeyField(Spec)
    systemId = ForeignKeyField(PlaneSystem)
    name = CharField(max_length=100, null=False)
    count_on_plane = IntegerField(default=1)
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'agregate_name_list'


class AgregateOnPlane(BaseModel):
    agregateId = ForeignKeyField(AgregateName)
    zavNum = CharField(max_length=100, null=True)
    dateVyp = DateField(null=True)
    planeId = ForeignKeyField(Plane)
    state = ForeignKeyField(AgregateState)

    class Meta:
        db_table = 'agregate_list'


def create_tables():
    with db:
        db.create_tables(
            [
                ListControl, ListControlExec, PlaneType, Unit, Spec, Plane, PlaneSystem, AgregateName,
                OsobPlane, AgregateState, RemZav, RemType, ZavIzg, AgregateOnPlane
            ]
        )
