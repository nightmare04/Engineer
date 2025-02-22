import json
from PyQt6 import QtSql
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase, JSONField

db = SqliteExtDatabase('./database/pw.db', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    id = PrimaryKeyField(null=False, unique=True)

    class Meta:
        database = db


class ListControl(BaseModel):
    tlg = CharField(max_length=100, null=False)
    tlg_date = DateField()
    tlg_deadline = DateField()
    description = TextField(null=True)
    lc_number = CharField(max_length=10, null=True)
    answer = CharField(max_length=100, null=True)
    answer_date = DateField(null=True)
    specs = JSONField()
    planes = JSONField()
    complete_flag = BooleanField(default=False)

    class Meta:
        db_table = 'list_controls'


class PlaneType(BaseModel):
    type = CharField(max_length=30, null=False)
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'plane_types'


class Unit(BaseModel):
    name = CharField(max_length=100, null=False)
    reglament = BooleanField(default=False)
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'units'


class Plane(BaseModel):
    type = ForeignKeyField(PlaneType, backref='planes')
    zav_num = CharField(max_length=30, null=False)
    bort_num = CharField(max_length=10, null=False)
    unit = ForeignKeyField(Unit, backref='planes')
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'planes'


class Spec(BaseModel):
    name = CharField(max_length=100, null=False)
    not_delete = BooleanField(default=True)

    class Meta:
        db_table = 'specs'


class ListControlExec(BaseModel):
    lc_id = ForeignKeyField(ListControl, backref='lcexec')
    plane_id = ForeignKeyField(Plane, backref='lcexec')
    spec_id = ForeignKeyField(Spec, backref='lcexec')
    date = DateField()

    class Meta:
        db_table = 'list_control_execs'


def create_tables():
    with db:
        db.create_tables(
            [
                ListControl, ListControlExec, PlaneType, Unit, Spec, Plane
            ]
        )


