import os
from pathlib import Path
from datetime import datetime
import json
import copy

def make_local():
    HOME = Path(os.environ["HOME"])
    LOCAL = HOME/".doctour"
    LOCAL.mkdir(exist_ok=True)
    return LOCAL
    
def logfile(logtype, mode = "w"):
    LOCAL = make_local()
    LOG = LOCAL/"log"
    LOG.mkdir(exist_ok=True)
    LOGFILE = LOG/logtype
    return LOGFILE.open(mode=mode)

def startup_log(**kwargs):
    log = copy.deepcopy(kwargs)
    log.update({
        "time":datetime.now().strftime("%Y%m%d_%H%M%S"),
        "user":os.environ.get("USER"),
        "home":os.environ.get("HOME"),
        })
    logstr = json.dumps(log)
    f = logfile("startapp")
    f.write("\n")
    f.write(logstr)
    f.close()
    return logstr
    