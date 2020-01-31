import pandas as pd
import inspect
from .doc import docModel, docGraphModel


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

class docTour(object):
    def __init__(self, root_obj, root_name,sess, load_source=False):
        self.docs = dict()
        self.root_obj = root_obj
        self.load_source = load_source
        self.sess = sess  # sqla session
        self.doc_parser(self.root_obj, root_name, name_chain=root_name)
        print(f"saving [{root_name}] basics to db")
        self.sess.commit()
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
            list(i.to_dicts("id","name", "doc", "path", "names", "level", "source") for i in self.docs.values()))
        return df

    def new_doc(self, name_chain, kid, parent, level):
        """
        New docModel object
        :param name_chain: name chain string
        :param kid: the subject new  obj
        :param parent: parent obj
        :param level: int, level from root obj
        :return: docModel object
        """
        sd = docModel(id=id(kid), name=name_chain.split(".")[-1], names=name_chain, level=level, doc=str(kid.__doc__),
                      path=get_path(kid))
        if self.load_source:
            sd.source = get_source(kid)
        self.sess.add(sd)

        if parent:
            dg = docGraphModel(parent_id=parent.id, kid_id=sd.id)
            self.sess.add(dg)
        return sd

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
            sd = self.new_doc(name_chain, obj, parent, level)
            self.docs[addr] = sd

        for attr_name in dir(obj):
            sub_obj = getattr(obj, attr_name)
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
                        print(f"[ERROR]>>{name_chain_},\t{e}")
