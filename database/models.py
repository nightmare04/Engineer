import json
from PyQt6 import QtSql
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


class VypZav(BaseModel):
    name = CharField(max_length=30, null=False)
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'vyp_zav'


class Plane(BaseModel):
    planeType = ForeignKeyField(PlaneType, backref='planes')
    zavNum = CharField(max_length=30, null=False)
    name = CharField(max_length=10, null=False)
    dateVyp = DateField()
    dateRem = DateField()
    remType = CharField(max_length=30, null=False)
    remZav = ForeignKeyField(RemZav)
    vypZav = ForeignKeyField(VypZav)
    osobPlane = JSONField()
    unit = ForeignKeyField(Unit, backref='planes')
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'planes'


class RemType(BaseModel):
    name = CharField(max_length=30, null=False)
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'rem_type'


class OsobPlane(BaseModel):
    planeType = ForeignKeyField(PlaneType)
    name = CharField(max_length=30, null=False)
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'osob_plane'


class Spec(BaseModel):
    name = CharField(max_length=100, null=False)
    planeType = ForeignKeyField(PlaneType)
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
    planeType = ForeignKeyField(PlaneType)
    specId = ForeignKeyField(Spec, backref='lcexec')
    name = CharField(max_length=100, null=False)
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'plane_systems'


class PlaneAgregate(BaseModel):
    planeSystem = ForeignKeyField(PlaneSystem)
    name = CharField(max_length=100, null=False)

    class Meta:
        db_table = 'plane_agregates'


class AgregateState(BaseModel):
    name = CharField(max_length=100, null=False)

    class Meta:
        db_table = 'agregate_states'


class AgregateOnPlane(BaseModel):
    planeAgregate = ForeignKeyField(PlaneAgregate)
    zavNum = CharField(max_length=100, null=True)
    dateVyp = DateField
    planeId = ForeignKeyField(Plane)
    state = ForeignKeyField(AgregateState)

    class Meta:
        db_table = 'agregates'


def create_tables():
    with db:
        db.create_tables(
            [
                ListControl, ListControlExec, PlaneType, Unit, Spec, Plane, PlaneSystem, PlaneAgregate,
                AgregateOnPlane, OsobPlane, AgregateState, RemZav, RemType, VypZav
            ]
        )
