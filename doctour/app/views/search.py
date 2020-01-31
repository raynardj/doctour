from flask_appbuilder  import BaseView, expose, ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask import jsonify, request
import json
import inspect
import logging
import importlib
from doctour.base.parse import docTour
from doctour.base.doc import docModel
from doctour.app.models.lib import libModel

from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine as ce
Session = sessionmaker()
class searchView(BaseView):
    route_base = "/search"

    @expose("/index/", methods = ["POST"])
    def major_view(self):
        data_ = json.loads(request.data)
        kw = data_["kw"]
        logging.info(kw)
        try:
            logging.info(f"loading {kw}")
            obj = __import__(kw)
            logging.info(f"{str(obj)} loaded")
        except Exception as e:
            return jsonify({
            "status":500, "success":False, "data":{"error":str(e)}
        })
        obj_info = dict({
            "name":kw,
            "file":inspect.getsourcefile(obj),
        })

        return jsonify({
            "status":200, "success":True, "data":obj_info
        })

class docView(ModelView):
    route_base = "/doc"
    datamodel = SQLAInterface(docModel)

    @expose("/read/<lib>/<doc_id>/",methods = ["GET"])
    def read_doc(self,lib,doc_id):
        return self.render_template("read_doc.html")

    @expose("/read/",methods = ["POST"])
    def read_api(self):
        dct = json.loads(request.data)
        doc_id = dct["id"]
        lib = dct["lib"]
        lib_item = self.appbuilder.session.query(libModel).filter(libModel.name==lib).first()
        eng = ce(lib_item.data)

        sess = Session(bind=eng)
        self.datamodel.session = sess
        item = self.datamodel.get(doc_id)
        return jsonify({
            "success":True,"status":200,
            "data":{"id":item.id, "name":item.name,"names":list(item.names.split(",")),"doc":item.doc.replace("\n","<br>"), "level":item.level, "path":item.path}
        })

    @expose("/list_all/",methods = ["POST","GET"])
    def read_all_api(self):
        alllibs = list({"text":i.name} for i in self.appbuilder.session.query(libModel).all())
        return jsonify({"status":200,"success":True if len(alllibs)>0 else False, "data":alllibs})