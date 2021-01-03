from protein import * 
from link import *
import networkx as nx
from time import strftime
from os import system, write

class GraphLib:
    def __init__ (self, _name="", _proteins=[], _links=[], _G=nx.Graph()):
        if _name=="":
            self.name=strftime("%Y%m%d%H%M%S")
        else:
            self.name=_name
        self.proteins=_proteins
        self.links=_links
        self.G=_G

    def new_name(self, n_name, recreate=True):
        old=self.name
        self.name=n_name
        if not old.endswith(".graphml"):
            old+=".graphml"
        if not n_name.endswith(".graphml"):
            n_name+=".graphml"
        system("mv saved/"+old+" saved/"+n_name)
        if recreate:
            self.create_nxGraph()

    def create_nxGraph(self, graph_name=""):
        if graph_name!="":
            self.new_name(graph_name)
        self.G=nx.DiGraph(title=self.name)
        for p in self.proteins:
            self.G.add_node(p.name, p.toDic())
        for l in self.links:
            self.G.add_edge(l.p1, l.p2)
        return self.G

    def open_graph(self, graph_name=""):
        if graph_name!="" and self.name!=graph_name:
            self.name=graph_name
        _name=self.name
        try:
            if not _name.endswith(".graphml"):
                _name+=".graphml"
            self.G=nx.read_graphml("saved/"+_name)
            return self.G
        except:
            os.write(1, "\033[91mCould not open graph "+self.name+"\033[0m\n".encode)
            return None

    def write_graph(self, graph_name=""):
        if graph_name!="":
            self.new_name(graph_name)
        _name=self.name
        try:
            if not _name.endswith(".graphml"):
                _name+=".graphml"
            
            nx.write_graphml(self.create_nxGraph(), "saved/"+_name)
            return True
        except:
            print("Could not write graph to "+name)
            return False

    #Proteins function
    def add_protein(self, new_p: Protein):
        l1=0
        l2=0
        if new_p not in self.proteins:
            self.proteins.append(new_p)
            self.create_nxGgraph()
            return(self.G, self.proteins)
        else:
            return (None, None)

    def find_protein(self, p1):
        for p in self.proteins:
            if p==p1:
                return p
        return None

    def remove_protein(self, _p):
        new_l=[]
        rm_p=find_protein(proteins, _p)
        for p in proteins:
            if p!=rm_p:
                new_l.append(p)
        self.proteins=new_l
        self.create_nxGraph()
        return self.proteins

    #Given two proteins, remove a link. Returns the new list.
    def remove_link_with_ps(self, _p1, _p2):
        p1=self.find_protein(_p1)
        p2=self.find_protein(_p2)
        rm_l=Link(p1, p2)
        new_l=[]
        for l in self.links:
            if l!=rm_l:
                new_l.append(l)
        self.links=new_l
        self.create_nxGraph()
        return self.links

    #Given a link, remove it. Returns the new list.
    def remove_link_with_l(self, rm_l):
        new_l=[]
        for l in links:
            if l!=rm_l:
                new_l.append(l)
        self.links=new_l
        self.create_nxGraph()
        return self.links
    
    #Given a list of links to remove, removes all of them and returns the new list.
    def remove_links(self, rm_ll):
        new_l=[]
        for l in links:
            if l not in rm_ll:
                new_l.append(l)
        self.links=new_l
        self.create_nxGraph()
        return new_l

    #Given a protein, return all links for which the protein is one of the edges. Returns the list of all links.
    def find_links(self, _p: Protein):
        p=self.find_protein(_p)
        new_l=[]
        for l in links:
            if l.p1==p or l.p2==p:
                new_l.append(l)
        return new_l





