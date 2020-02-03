from flask_appbuilder import BaseView, expose, ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask import jsonify, request
import json
import inspect
import logging
import importlib
from doctour.base.parse import docTour
from doctour.base.doc import docModel,docGraphModel,inhGraphModel
from doctour.app.models.lib import libModel

from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine as ce

Session = sessionmaker()


class searchView(BaseView):
    route_base = "/search"

    @expose("/index/", methods=["POST"])
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
                "status": 500, "success": False, "data": {"error": str(e)}
            })
        obj_info = dict({
            "name": kw,
            "file": inspect.getsourcefile(obj),
        })

        return jsonify({
            "status": 200, "success": True, "data": obj_info
        })

class docView(ModelView):
    route_base = "/doc"
    datamodel = SQLAInterface(docModel)

    @expose("/read/<lib>/<doc_id>/", methods=["GET"])
    def read_doc(self, lib, doc_id):
        return self.render_template("read_doc.html")

    def item_dict(self,item):
        return dict({"id":item.id, "name":item.name,"alias": item.alias,"ctype":item.ctype})

    def get_lib(self,libname):
        lib_item = self.appbuilder.session.query(libModel).filter(libModel.name == libname).first()
        return lib_item

    @expose("/traceup/<lib>/<doc_id>/", methods=["POST","GET"])
    def trace_up(self, lib, doc_id):
        lib_item = self.get_lib(lib)
        eng = ce(lib_item.data)
        sess = Session(bind=eng)
        item = sess.query(docModel).filter(docModel.id==doc_id).first()
        return jsonify({"status":200, "success":True, "data":self.trace_up_parse(item)})

    def trace_up_parse(self,item):
        attrs = dict((i.id, self.item_dict(i)) for i in item.kids)
        rt = []
        for anc in item.ancs:
            result = self.trace_up_parse(anc)
            rt+=result
        attr_id = list(attrs.keys())
        for i in rt:
            for aid in attr_id:
                if aid in i["attrs"]:
                    del attrs[aid]
        thisdt = self.item_dict(item)
        thisdt.update({"attrs": attrs})
        rt = list([thisdt,])+rt
        return rt

    @expose("/read/", methods=["POST"])
    def read_api(self):
        dct = json.loads(request.data)
        doc_id = dct["id"]
        lib = dct["lib"]
        lib_item = self.get_lib(lib)
        eng = ce(lib_item.data)

        sess = Session(bind=eng)
        self.datamodel.session = sess
        item = self.datamodel.get(doc_id)
        kids = list(self.item_dict(i) for i in item.kids)
        parents = list(self.item_dict(i) for i in item.parents)
        dess = list(self.item_dict(i) for i in item.dess)
        ancs = list(self.item_dict(i) for i in item.ancs)
        return jsonify({
            "success": True, "status": 200,
            "data": {"id": item.id,
                     "name": item.name,
                     "names": list(item.names.split(",")),
                     "ctype":item.ctype,
                     "doc": item.doc,#.replace("\n", "<br>"),
                     "level": item.level,
                     "path": item.path,
                     "code": item.code if item.code!="" else "",
                     "kids": kids,
                     "parents": parents,
                     "dess": dess,
                     "ancs": ancs,
                     "lib": lib,
                     "alias":item.alias,
                     }
        })

    @expose("/list_all/", methods=["POST", "GET"])
    def read_all_api(self):
        """
        list all libraries
        :return:
        """
        alllibs = list(
            {"text": i.name, "a": f"/doc/lib/{i.name}/"} for i in self.appbuilder.session.query(libModel).all())
        return jsonify({"status": 200, "success": True if len(alllibs) > 0 else False, "data": alllibs})

    @expose("/lib/<libname>/", methods=["GET"])
    def get_lib_page(self, libname):
        lib_item = self.get_lib(libname)
        eng = ce(lib_item.data)
        sess = Session(bind=eng)
        context = dict({
            "lib":libname,
            "total":sess.query(docModel).count(),
            "classes":sess.query(docModel).filter(docModel.ctype=="class").count(),
            "functions": sess.query(docModel).filter(docModel.ctype == "function").count(),
            "modules": sess.query(docModel).filter(docModel.ctype == "module").count(),
            "attr_relations":sess.query(docGraphModel).count(),
            "inheritance": sess.query(inhGraphModel).count(),
        })
        return self.render_template("lib.html", **context)

    @expose("/code/", methods=["POST"])
    def get_code(self):
        dt = json.loads(request.data)
        lib = dt["lib"]
        name_chain = list(dt["name_chain"].split("."))[1:]
        try:
            obj = __import__(lib)
        except:
            return jsonify({"status":500, "success":False,
                })
        for att in name_chain:
            obj = getattr(obj,att)

        try:
            code  = inspect.getsource(obj)
        except:
            code = "None"
        return jsonify({"status":200, "success":True,
                "data":
                    {"code":code}
                })


