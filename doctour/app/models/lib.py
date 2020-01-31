from flask_appbuilder import Model
from sqlalchemy import Column, Integer, Text
from flask_appbuilder.models.mixins import AuditMixin
from .. import db

class libModel(db.Model):
    __tablename__ = "libs"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text())
    data = db.Column(db.Text())