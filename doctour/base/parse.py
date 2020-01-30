import pandas as pd
import inspect

class singleDoc(object):
    def __init__(self, name, doc="", level=-1):
        self.name = name.split(".")[-1]
        self.doc = doc if doc else ""
        self.parents = []
        self.kids = []
        self.names = []
        self.names.append(name)
        self.level = level
        self.source = ""

    def __repr__(self):
        return f"<{self.name}>"

    #         return f"""
    #         [Name:\t{self.name}][Level:\t{self.level}][Names:{len(self.names)}]
    #         """

    def new_parent(self, parent):
        if parent:
            self.parents.append(parent)
            parent.kids.append(self)

    def new_name(self, nname):
        self.names.append(nname)

    def to_dicts(self, *cols):
        return dict((col, getattr(self, col)) for col in cols)


def mv_attr(*args):
    args_kv = dict((a,f"__{a}__") for a in args)
    def move(src,dst):
        for da,sa in args_kv.items():
            if hasattr(src, sa):
                setattr(dst, da, getattr(src, sa))
    return move

def get_source(obj):
    try: return inspect.getsource(obj)
    except: return ""


moves = mv_attr("doc")


class docTour(object):
    def __init__(self, root_obj, root_name, load_source=False):
        self.docs = dict()
        self.root_obj = root_obj
        self.load_source = load_source
        self.doc_parser(self.root_obj, root_name, name_chain=root_name)
        self.df = self.to_df()

    def mid(self, obj):
        """
        memory address
        """
        return hex(id(obj))

    def sort_score(self, df, score_field="score"):
        return df.sort_values(by=score_field, ascending=False)

    def sch_name_short(self, nm):
        return self.sort_score(self.df[self.df.name.str.contains(nm)])

    def to_df(self):
        df = pd.DataFrame(
            list(i.to_dicts("name", "doc", "parents", "kids", "names", "level", "source") for i in self.docs.values()))
        df["p_ct"] = df.parents.apply(len)
        df["k_ct"] = df.kids.apply(len)
        df["score"] = df["k_ct"] + df["p_ct"] - df["level"] * 2
        return df

    def doc_parser(self, obj, name, level=0, name_chain="", parent=None):
        """
        Parse the sub structure of an object and tracing its documentation
        obj: python class/ object /function
        name: str, name of the object
        level:int, level count from the root obj
        name_chain: str
        parent: singleDoc,
        """
        addr = self.mid(obj)
        if addr in self.docs:
            if type(self.docs[addr]) == singleDoc:
                sd = self.docs[addr]
                sd.new_name(name_chain)
                sd.new_parent(parent)
            return None

        if hasattr(obj, "__doc__"):
            sd = singleDoc(name_chain, level=level, )
            moves(obj, sd)
            sd.new_parent(parent)
            if self.load_source:
                sd.source = get_source(obj)
            self.docs[addr] = sd

        for attr_name in dir(obj):
            sub_obj = getattr(obj, attr_name)
            name_chain_ = name_chain + "." + attr_name
            if self.mid(sub_obj) in self.docs:
                sd = self.docs[self.mid(sub_obj)]
                sd.new_name(name_chain_)
                sd.new_parent(self.docs[addr])
                if self.load_source:
                    sd.source = get_source(sub_obj)
                continue
            elif "__" not in attr_name:
                if level < 6:
                    try:
                        self.doc_parser(getattr(obj, attr_name), attr_name, level=level + 1, name_chain=name_chain_,
                                        parent=self.docs[addr])
                    except Exception as e:
                        print(f"[ERROR]>>{name_chain_}")