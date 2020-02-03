from flask_appbuilder import ModelView,expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask import jsonify,request
import json
from doctour.app.models.lib import libModel
from doctour.base.doc import docModel,docGraphModel,inhGraphModel
from doctour.base.parse import docTour, parse_lib
import importlib
import os
import logging
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine as ce
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
        
        if "dataurl" in dt:
            dataurl = dt["dataurl"]
            self.add_lib_record(lib,dataurl)
        check_lib = list(self.appbuilder.session.query(libModel).filter(libModel.name == lib).all())
        if len(check_lib)>0:
            return jsonify({"status":200,"success":True, "data":{
                "frame":pd.read_sql("SELECT id,name,ctype,alias from docs",con=ce(check_lib[0].data).connect()).to_dict(orient="record")
            }})
        else:
            logging.info(f"parsing {lib}")
            dt, dataurl= parse_lib(lib, import_ = True)
            self.add_lib_record(lib,dataurl)
            rt = {"status": 200, "success": True, "data": {
                "rows": len(dt), "frame": dt.df.to_dict(orient="record")
             }}
        return jsonify(rt)

    def add_lib_record(self,lib,dataurl):
        self.appbuilder.session.add(libModel(name=lib, data=dataurl))
        self.appbuilder.session.commit()

    