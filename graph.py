from protein import Protein
from link import Link
import networkx as nx
from time import strftime
from os import system
import os
import numpy as np 
import holoviews as hv
from holoviews import opts

class GraphLib:
    def __init__ (self, _name="", _proteins=[], _links=[], _G=nx.Graph()):
        if _name=="":
            self.name=strftime("%Y%m%d%H%M%S")
        else:
            self.name=_name
        self.proteins=_proteins
        self.links=_links
        self.G=_G
        self.pCounter=0 #Yeah I know it's ugly, but c'mon

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
            self.G.add_node(p.name, pid=p.pid, color=p.color, description=p.description)
        for l in self.links:
            self.G.add_edge(str(l.p1), str(l.p2), color=l.color, description=l.description)
        return self.G

    def hvGraph(self):
        nxPos=nx.fruchterman_reingold_layout(self.create_nxGraph())

        p_colors=[]
        x=[]
        y=[]
        p_names=[]
        p_descriptions=[]
        p_ids=[]
        for p in self.proteins:
            p_colors.append(p.color)
            x.append(nxPos[p.name][0])
            y.append(nxPos[p.name][1])
            p_names.append(p.name)
            p_ids.append(p.pid)
            p_descriptions.append(p.description)

        l_colors=[]
        l_descriptions=[]
        source=[]
        target=[]
        for l in self.links:
            l_colors.append(l.color)
            source.append(l.p1.pid)
            target.append(l.p2.pid)
            l_descriptions.append(l.description)
        l_ids=np.arange(0, len(l_colors))

        nodes = hv.Nodes((x, y, p_ids, p_names, p_descriptions), vdims=['Name', 'Description'])
        graph = hv.Graph(((source, target, l_ids, l_descriptions), nodes), vdims=['l_id', 'Description']).opts(tools=['hover','tap'],
                   node_color='index',
                   cmap = p_colors,
                   edge_color="l_id",
                   edge_cmap= l_colors,
                   xaxis=None, yaxis=None
                  )
        return graph

    def open_graph(self, graph_name=""):
        if graph_name!="" and self.name!=graph_name:
            self.name=graph_name
        _name=self.name
        os.write(1, ("_name: "+_name+"\n").encode())
        if not _name.endswith(".graphml"):
            _name+=".graphml"
        os.write(1, ("_name: "+_name+"\n").encode())
        try:
            self.G=nx.read_graphml("saved/"+_name)
        except:
            os.write(1, ("\033[91mCould not open graph "+_name+"\033[0m\n").encode())
            return None
        #Get proteins and counter
        nxProteins=list(self.G.nodes(data=True))
        _counter=0;
        newProteins=[]
        for p in nxProteins:
            os.write(1, (str(p)+"\n").encode())
            p_color="#000000"
            p_descr=""
            try:
                p_color=p[1]['color']
            except:
                os.write(1, ("Could not get color for protein "+p[0]).encode())
            try:
                p_descr=p[1]['description']
            except:
                os.write(1, ("Could not get description for protein "+p[0]).encode())
            
            newP=Protein(int(p[1]['pid']), p[0], p_color, p_descr)
            newProteins.append(newP)
            if newP.pid>_counter:
                _counter=newP.pid
        self.pCounter=_counter+1
        self.proteins=newProteins
        #Get links between proteins
        nxLinks=list(self.G.edges.data())
        newLinks=[]
        for e in nxLinks:
            p1=self.find_protein(e[0])
            p2=self.find_protein(e[1])
            l_color="#000000"
            l_descr=""
            try:
                l_color=e[2]['color']
            except:
                os.write(1, ("Cannot get link color for link between "+p1.name+" and "+p2.name+"\n").encode())
            try:
                l_descr=e[2]['description']
            except:
                os.write(1, ("Cannot get link description for link between "+p1.name+" and "+p2.name+"\n").encode())
            
            newL=Link(p1, p2, l_color, l_descr)
            newLinks.append(newL)
        self.links=newLinks

        return self

    def write_graph(self, graph_name=""):
        os.write(1, "Writing graph\n".encode())
        if graph_name!="":
            self.new_name(graph_name)
        _name=self.name
        try:
            if not _name.endswith(".graphml"):
                _name+=".graphml"
            
            nx.write_graphml(self.create_nxGraph(), "saved/"+_name)
            os.write(1, ("Wrote graph "+_name+" #p="+str(len(self.proteins))+" #l="+str(len(self.links))+"\n").encode())
            return True
        except:
            os.write(1, ("Could not write graph to "+name).encode())
            return False

    #Proteins function
    def add_protein(self, new_p: Protein):
        if new_p not in self.proteins:
            new_p.pid=self.pCounter
            self.pCounter+=1
            self.proteins.append(new_p)
            self.create_nxGraph()
            os.write(1, (new_p.name+" "+new_p.color).encode())
            return(self.G, self.proteins)
        else:
            return (None, None)

    #Returns the protein if it's in the list, None otherwise
    def find_protein(self, p1):
        for p in self.proteins:
            if p==p1:
                return p
        return None
    
    #Given a protein, removes it from the list. Returns the new list.
    #NOTE: checks about protein's existence should be made prior to function invocation, hence, rm_p is required to be `Protein`. 
    def remove_protein(self, rm_p : Protein):
        #Create new list
        new_pl=[]
        for p in self.proteins:
            if p!=rm_p:
                new_pl.append(p)
        self.proteins=new_pl
        #Remove all links containing protein.
        lrm=self.find_links(rm_p)
        self.links=self.remove_links(self.find_links(rm_p)) #This should be redundant
        
        self.create_nxGraph()
        return self.proteins

    #Links function
    def add_link(self, link: Link):
        if link not in self.links:
            self.links.append(link)
            self.create_nxGraph()
            return (self.G, self.links)
        else:
            return (None, None)

    #Given two proteins, remove a link. Returns the new list.
    #NOTE: checks about proteins existence should be made prior to function invocation. 
    def remove_link_with_ps(self, _p1 : Protein, _p2 : Protein):
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
        for l in self.links:
            if l!=rm_l:
                new_l.append(l)
        self.links=new_l
        self.create_nxGraph()
        return self.links
    
    #Given a list of links to remove, removes all of them and returns the new list.
    def remove_links(self, rm_ll):
        new_l=[]
        for l in self.links:
            if l not in rm_ll:
                new_l.append(l)
        self.links=new_l
        self.create_nxGraph()
        return new_l
    
    #Given two proteins, returns the link between the two proteins if it exists, None otherwise.
    def find_link(self, _p1: Protein, _p2: Protein):
        p1=self.find_protein(_p1)
        p2=self.find_protein(_p2)
        new_l=[]
        for l in self.links:
            if l.p1==p1 and l.p2==p2:
                return l
        return None

    #Given a protein, return all links for which the protein is one of the edges. Returns the list of all links.
    #NOTE: checks about protein existence are to be made prior to this function invocation. 
    def find_links(self, p: Protein):
        new_l=[]
        for l in self.links:
            if l.p1==p or l.p2==p:
                new_l.append(l)
        return new_l





