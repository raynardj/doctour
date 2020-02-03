import requests
from doctour.base.utils import logfile
from doctour.base.parse import docTour, parse_lib
import json
from datetime import datetime
import logging
from doctour.base.parse import checks

class exam(object):
    def __init__(self, obj, host = "localhost"):
        self.obj = obj
        self.host = host
        self.port = self.doctour_log["port"]
        self.parse()

    @property
    def doctour_log(self):
        f = logfile("startapp","r")
        jsonstr = f.readlines()[-1]
        return json.loads(jsonstr)

    def get_obj_name(self, obj):
        name = str(obj)
        if hasattr(obj, "__name__"):
            name = obj.__name__
        if hasattr(obj, "__code__"):
            if hasattr(obj, "co_name"):
                name = obj.__code__.co_name
        return name

    def parse(self):
        if checks(self.obj)==False:
            self.obj = self.obj.__class__
        try:
            name = self.get_obj_name(self.obj)
        except:
            name = "object"
        name = f"{name}_{datetime.now().strftime('%H%M%S')}"
        self.name = name
        dt, dataurl = parse_lib(name, import_ = False, obj=self.obj)
        self.dt = dt
        url=f"http://{self.host}:{self.port}/lib/add/"
        dt_ = {"lib":name, "dataurl":dataurl}
        logging.info(url)
        logging.info(str(dt_))
        r = requests.post(url, data=json.dumps(dt_))
        if r.status_code == 200:
            data = r.json()["data"]["frame"]
        self.data  = data
        for d in data:
            if d["name"] == name:
                print(f"please visit http://{self.host}:{self.port}/doc/read/{d['name']}/{d['id']}/")
                return d
        print("Parsing not through")

    def __repr__(self):
        return f"<DocTour:{self.name}>"

