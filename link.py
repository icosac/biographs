from protein import *

class Link:
    def __init__(self, _p1: Protein, _p2: Protein, _color="", _description=""):
        self.p1=_p1
        self.p2=_p2
        self.color=_color
        self.description=_description

    def __eq__(self, other):
        if other==None:
            return False
        else:
            return (other!=None and self.p1==other.p1 and self.p2==other.p2)

    def __lt__(self, other):
        return self.p1<other.p1

    def __str__(self):
        return "<"+str(self.p1)+" -- "+str(self.p2)+">"










