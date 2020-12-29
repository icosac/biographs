from protein import *

class Link:
    def __init__(self, _p1, _p2, _color="", _description=""):
        self.p1=_p1
        self.p2=_p2
        self.color=_color
        self.description=_description

    def __eq__(self, other):
        return (self.p1==other.p1 and self.p2==other.p2)

    def __str__(self):
        return "<"+str(self.p1)+", "+str(self.p2)+">"

#Given two proteins, remove a link. Returns the new list.
def remove_link_with_ps(links, proteins, _p1, _p2):
    p1=find_protein(proteins, _p1)
    p2=find_protein(proteins, _p2)
    rm_l=Link(p1, p2)
    new_l=[]
    for l in links:
        if l!=rm_l:
            new_l.append(l)
    return new_l

#Given a link, remove it. Returns the new list.
def remove_link_with_l(links, rm_l):
    new_l=[]
    for l in links:
        if l!=rm_l:
            new_l.append(l)
    return new_l

def remove_links(links, rm_ll):
    new_l=[]
    for l in links:
        if l not in rm_ll:
            new_l.append(l)
    return new_l

#Given a protein, return all links for which the protein is one of the edges. Returns the list of all links.
def find_links(links, proteins, _p):
    p=find_protein(proteins, _p)
    new_l=[]
    for l in links:
        if l.p1==p or l.p2==p:
            new_l.append(l)
    return new_l

#Given a protein, return all links for which the protein is one of the edges. Returns the list of all links.
def find_links(links, p):
    new_l=[]
    for l in links:
        if l.p1==p or l.p2==p:
            new_l.append(l)
    return new_l









