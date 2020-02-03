import pandas as pd
import inspect
from doctour.base.doc import docModel, docGraphModel, inhGraphModel
import logging
from sqlalchemy import create_engine as ce
from sqlalchemy.orm.session import sessionmaker
import os
Session = sessionmaker()
basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))+"/app/dbs"
def most_frequent(List): return max(set(List), key = List.count)
def get_source(obj):
    try:
        return inspect.getsource(obj)
    except:
        return ""


def get_path(obj):
    try:
        return inspect.getsourcefile(obj)
    except:
        return ""

def checks(obj):
    if inspect.ismodule(obj):return "module"
    if inspect.isclass(obj):return "class"
    if inspect.isfunction(obj):return "function"
    return False

class docTour(object):
    def __init__(self, root_obj, root_name,sess, load_source=False):
        self.docs = dict()
        self.inh_cache = set()
        self.sd_list = list()
        self.root_obj = root_obj
        self.load_source = load_source
        self.sess = sess  # sqla session
        self.doc_parser(self.root_obj, root_name, name_chain=root_name)
        self.vote_name()
        logging.info(f"{len(self.docs)} things found")
        logging.info(f"saving [{root_name}] basics to db")
        self.sess.commit()
        logging.info(f"creating df for [{root_name}]")
        self.df = self.to_df()

    def __len__(self):
        return len(self.docs)

    def mid(self, obj):
        """
        memory address
        """
        return id(obj)

    def to_df(self):
        df = pd.DataFrame(
            list(i.to_dicts("id","name", "doc", "path", "names", "level", "source","ctype","alias") for i in self.docs.values()))
        return df

    def new_doc(self, name_chain, kid, parent, level,ctype):
        """
        New docModel object
        :param name_chain: name chain string
        :param kid: the subject new  obj
        :param parent: parent obj
        :param level: int, level from root obj
        :return: docModel object
        """
        sd = docModel(id=id(kid), name=name_chain.split(".")[-1],
                      names=name_chain, level=level, doc=str(kid.__doc__),
                      ctype = ctype,
                      )
        if ctype=="function":
            path = kid.__code__.co_filename
            if path[-3:] == ".py":
                sd.path = path
                sd.code = inspect.getsource(kid)
        else:
            sd.path = get_path(kid)
        if ctype=="class":
            self.parse_inh(kid)
        if self.load_source:
            sd.source = get_source(kid)

        self.sess.add(sd)
        self.sd_list.append(sd)

        if parent:
            dg = docGraphModel(parent_id=parent.id, kid_id=sd.id)
            self.sess.add(dg)
        return sd

    def parse_inh(self,obj):
        addr = self.mid(obj)
        if addr in self.inh_cache:
            return None
        elif hasattr(obj,"__bases__"):
            bases = obj.__bases__
            if len(bases) == 0: return None

            for b in bases:
                name = obj.__name__
                ig = inhGraphModel(anc_id=id(b), des_id=addr)
                self.sess.add(ig)
                self.parse_inh(b)
                if id(b) not in self.docs:
                    self.doc_parser(b,name,level=1, name_chain=name, parent=None)

            self.inh_cache.add(addr)

    def doc_parser(self, obj, name, level=0, name_chain="", parent=None):
        """
        Parse the sub structure of an object and tracing its documentation
        obj: python class/ object /function
        name: str, name of the object
        level:int, level count from the root obj
        name_chain: str
        parent: docModel,
        """
        addr = self.mid(obj)
        ctype = checks(obj)
        if ctype == False: return None
        if addr in self.docs:
            if type(self.docs[addr]) == docModel:
                sd = self.docs[addr]
                sd.names = sd.names +"," + name_chain
                self.sess.add(sd)
                if parent:
                    dg = docGraphModel(parent_id=parent.id, kid_id=sd.id)
                    self.sess.add(dg)
            return None

        if hasattr(obj, "__doc__"):
            sd = self.new_doc(name_chain, obj, parent, level, ctype)
            self.docs[addr] = sd

        for attr_name in dir(obj):
            sub_obj = getattr(obj, attr_name)
            if checks(sub_obj)==False: continue
            name_chain_ = name_chain + "." + attr_name
            if self.mid(sub_obj) in self.docs:
                sd = self.docs[self.mid(sub_obj)]
                sd.names = sd.names +","+ name_chain_

                if self.load_source:
                    sd.source = get_source(sub_obj)
                self.sess.add(sd)
                if parent:
                    dg = docGraphModel(parent_id=self.docs[addr].id, kid_id=sd.id)
                    self.sess.add(dg)
                continue
            elif "__" not in attr_name:
                if level < 6:
                    try:
                        self.doc_parser(getattr(obj, attr_name), attr_name, level=level + 1, name_chain=name_chain_,
                                        parent=self.docs[addr])
                    except Exception as e:
                        logging.error(f"{name_chain_},\t{e}")

    def vote_name(self):
        logging.info("start voting for most frequent name")
        for sd in self.sd_list:
            name_list = list(n.split(".")[-1] for n in sd.names.split(","))
            sd.name = most_frequent(name_list)
            sd.alias = ",".join(set(name_list))
            self.sess.add(sd)
        logging.info("voting complete")

def parse_lib(lib, import_ = True, obj = None):
    path = os.path.join(basedir, f"{lib}.db")
    dataurl = "sqlite:///" + path
    os.system(f"rm {path}")
    logging.info(f"creating SQLite db:\t {dataurl}")
    eng = ce(dataurl)
    sess = Session(bind=eng)

    for m in [docModel,docGraphModel,inhGraphModel]:
        refresh_table(m, engine = eng)

    if import_:
        dt = docTour(__import__(lib), lib, sess)
    else:
        dt = docTour(obj, lib, sess)
    return dt,dataurl

def refresh_table(model,engine):
    table = model.__table__
    if table.exists(engine):
        logging.info(f"dropping existing table: {str(table)}")
        table.drop(engine)
    logging.info(f"creating a new table: {str(table)}")
    table.create(engine)