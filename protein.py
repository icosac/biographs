class Protein:
    def __init__(self, _id, _name, _color="black", _description=""):
        self.id
        self.name=_name
        self.color=_color
        self.description=_description

    def __lt__(self, other):
        return self.name<other.name

    def __eq__(self, other):
        return self.name==other.name

    def __str__(self):
        return self.name

    def toDic(self):
        return {"id" : self.id, "name" : self.name, "color" : self.color, "description" : self.description}

def add_protein(G, proteins, new_p: Protein):
    l1=0
    l2=0
    if G!=None:
        l1=len(G.nodes)
    if proteins!=None:
        l1=len(proteins)
    if l1==l2 and G!=None and proteins!=None:
        G.add_node(new_p.name, new_p.toDic())
        proteins.append(new_p)
    elif l1==l2-1 and G!=None:
        G.add_node(new_p.name, new_p.toDic())
    elif l1==l2+1 and proteins!=None:
        proteins.append(new_p)
    else:
        return (None, None)
    return (G, proteins)

def find_protein(proteins, p1):
    for p in proteins:
        if p==p1:
            return p
    return None

def remove_protein(proteins, _p):
    new_l=[]
    rm_p=find_protein(proteins, _p)
    for p in proteins:
        if p!=rm_p:
            new_l.append(p)
    return new_l

