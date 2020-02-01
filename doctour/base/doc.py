# from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Text, Integer, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
from flask_appbuilder import Model
from sqlalchemy.orm import relationship

class docModel(Model):
    __tablename__ = "docs"
    id = Column(Integer, primary_key = True, autoincrement=False)
    name = Column(Text())
    doc = Column(Text(), default = "")
    names = Column(Text(), default="")
    level = Column(Integer(),default = -1)
    source = Column(Text(), default = "")
    path = Column(Text(), default="")

    def __repr__(self):
        return f"<{self.name}>"

    def new_parent(self, parent):
        if parent:
            self.parents.append(parent)
            parent.kids.append(self)

    def new_name(self, nname):
        self.names.append(nname)

    def to_dicts(self, *cols):
        return dict((col, getattr(self, col)) for col in cols)

class docGraphModel(Model):
    __tablename__ = "doc_graph"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer(), ForeignKey("docs.id") )
    parent = relationship(docModel, foreign_keys = [parent_id] )
    kid_id = Column(Integer(), ForeignKey("docs.id"))
    kid = relationship(docModel, foreign_keys=[kid_id])

docModel.kids = relationship(docModel,
                             secondary = "doc_graph",
                             primaryjoin = (docModel.id == docGraphModel.parent_id),
                             secondaryjoin = (docGraphModel.kid_id == docModel.id)
                             )
docModel.parents = relationship(docModel,
                             secondary = "doc_graph",
                             primaryjoin = (docModel.id == docGraphModel.kid_id),
                             secondaryjoin = (docGraphModel.parent_id == docModel.id)
                             )
# docModel.parents = relationship(docModel, secondary = "doc_graph")