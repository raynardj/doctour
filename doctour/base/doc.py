# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_sql_orm.ipynb (unless otherwise specified).

__all__ = ['docModel', 'docGraphModel', 'inhGraphModel']

# Comes from python_parse.ipynb, cell
from sqlalchemy import Column, Text, Integer, ForeignKey
from flask_appbuilder import Model
from sqlalchemy.orm import relationship

# Comes from python_parse.ipynb, cell
class docModel(Model):
    __tablename__ = "docs"
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(Text())
    doc = Column(Text(), default="")
    names = Column(Text(), default="")
    level = Column(Integer(), default=-1)
    source = Column(Text(), default="")
    path = Column(Text(), default="")
    code = Column(Text(), default="")
    ctype = Column(Text(), default="")
    alias = Column(Text(), default="")

    def __repr__(self):
        return f"<{self.name}>"

    def new_parent(self, parent):
        if parent:
            self.parents.append(parent)
            parent.kids.append(self)

    def to_dicts(self, *cols):
        return dict((col, getattr(self, col)) for col in cols)

# Comes from python_parse.ipynb, cell
class docGraphModel(Model):
    __tablename__ = "doc_graph"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer(), ForeignKey("docs.id"))
    parent = relationship(docModel, foreign_keys=[parent_id])
    kid_id = Column(Integer(), ForeignKey("docs.id"))
    kid = relationship(docModel, foreign_keys=[kid_id])

# Mapping the self-relate docs on attribute relations
docModel.kids = relationship(docModel,
                             secondary="doc_graph",
                             primaryjoin=(docModel.id == docGraphModel.parent_id),
                             secondaryjoin=(docGraphModel.kid_id == docModel.id)
                             )
docModel.parents = relationship(docModel,
                                secondary="doc_graph",
                                primaryjoin=(docModel.id == docGraphModel.kid_id),
                                secondaryjoin=(docGraphModel.parent_id == docModel.id)
                                )

# Comes from python_parse.ipynb, cell
class inhGraphModel(Model):
    __tablename__ = "inh_graph"
    id = Column(Integer, primary_key=True)
    anc_id = Column(Integer(), ForeignKey("docs.id")) # ancestor
    anc = relationship(docModel, foreign_keys=[anc_id])
    des_id = Column(Integer(), ForeignKey("docs.id")) # descendant
    des = relationship(docModel, foreign_keys=[des_id])

# Mappping the self-relate docs on class inheritance
docModel.dess = relationship(docModel,
                             secondary="inh_graph",
                             primaryjoin=(docModel.id == inhGraphModel.anc_id),
                             secondaryjoin=(inhGraphModel.des_id == docModel.id)
                             )
docModel.ancs = relationship(docModel,
                                secondary="inh_graph",
                                primaryjoin=(docModel.id == inhGraphModel.des_id),
                                secondaryjoin=(inhGraphModel.anc_id == docModel.id)
                                )