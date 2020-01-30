from flask_appbuilder  import BaseView, expose
from flask import jsonify, request
import json
import inspect
import logging
import importlib
from doctour.base.parse import docTour

class searchView(BaseView):
    route_base = "/search"

    @expose("/index/", methods = ["POST"])
    def major_view(self):
        logging.info(request.data)
        data_ = json.loads(request.data)
        kw = data_["kw"]
        try:
            obj = importlib.import_module(kw)
        except Exception as e:
            return jsonify({
            "status":500, "success":False, "data":{"error":str(e)}
        })
        obj_info = dict({
            "name":kw,
            "file":inspect.getsourcefile(obj),
        })

        if hasattr(obj,"__doc__"):
            obj_info.update({"doc":obj.__doc__.replace("\n","<br>")})
        return jsonify({
            "status":200, "success":True, "data":obj_info
        })