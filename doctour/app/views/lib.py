from flask_appbuilder import ModelView,expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask import jsonify,request
import json
from doctour.app.models.lib import libModel
from doctour.base.doc import docModel,docGraphModel,inhGraphModel
from doctour.base.parse import docTour
import importlib
import os
import logging
from sqlalchemy import create_engine as ce
from sqlalchemy.orm.session import sessionmaker
import pandas as pd

basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))+"/dbs"
Session = sessionmaker()

class libView(ModelView):
    route_base = "/lib"
    datamodel = SQLAInterface(libModel)

    @expose("/add/", methods=["POST"])
    def doc(self):
        dt = json.loads(request.data)
        lib = dt["lib"]
        check_lib = list(self.appbuilder.session.query(libModel).filter(libModel.name == lib).all())
        if len(check_lib)>0:
            return jsonify({"status":200,"success":True, "data":{
                "frame":pd.read_sql("SELECT id,name,ctype,alias from docs",con=ce(check_lib[0].data).connect()).to_dict(orient="record")
            }})
        else:
            logging.info(f"parsing {lib}")
            dt = self.parse_lib(lib)
            rt = {"status": 200, "success": True, "data": {
                "rows": len(dt), "frame": dt.df.to_dict(orient="record")
             }}
        return jsonify(rt)

    def parse_lib(self, lib):
        dataurl = "sqlite:///" + os.path.join(basedir, f"{lib}.db")

        self.appbuilder.session.add(libModel(name=lib, data=dataurl))
        self.appbuilder.session.commit()

        os.system(f"rm {dataurl}")
        eng = ce(dataurl)
        sess = Session(bind=eng)

        for m in [docModel,docGraphModel,inhGraphModel]:
            self.refresh_table(m, engine = eng)

        dt = docTour(importlib.import_module(lib), lib, sess)
        return dt

    def refresh_table(self, model,engine):
        table = model.__table__
        if table.exists(engine):
            logging.info(f"dropping existing table: {str(table)}")
            table.drop(engine)
        logging.info(f"creating a new table: {str(table)}")
        table.create(engine)