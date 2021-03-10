##Function to choose second selection, i.e., actions on 

from ipywidgets import widgets
from IPython.display import display, clear_output
from ipyfilechooser import FileChooser
import holoviews as hv
import networkx as nx

from protein import *
from link import *
from graph import GraphLib


def printL(l):
    print("[", end="")
    for e in l:
        print(str(e), end=", ")
    print("]")
    
message=""
justOpened=True
G=nx.Graph()
mygraph=GraphLib()
hvGrahDisplay = display(display_id='hvGraph')
#a=mygraph.create_nxGraph()

graph_title=widgets.Text(description="Title:")
choice_w=widgets.Dropdown(options=[
        ("Add protein", 1), 
        ("Add link", 2), 
        ("Remove protein", 3), 
        ("Remove link", 4),
        ("List proteins", 5),
        ("List links", 6),
        ("List proteins and links", 7),
        ("Show graph", 8),
        ("Save graph as image", 9),
        #("Export graph to file", 10),
        #("Recover from file", 11)], 
    ], 
    value=1)
text_p_name=widgets.Text(description="Name: ")
text_description=widgets.Text(description="Description: ")
color_w=widgets.ColorPicker(concise=False, value="black", description="Color: ")
text_p1_link=widgets.Dropdown(options=sorted(mygraph.proteins), description="From: ")
text_p2_link=widgets.Dropdown(options=sorted(mygraph.proteins), description="To: ")
dropdown_proteins=widgets.Dropdown(options=sorted(mygraph.proteins), description="Name: ")
button_w=widgets.Button(icon="check", description="Save")
button_remove_w=widgets.Button(icon="times", description="Remove")
path_chooser_w=FileChooser(show_only_dirs=True, title="Choose where to save image: ")
widgetsL=[choice_w, text_p_name, text_description, color_w, text_p1_link, text_p2_link, dropdown_proteins, button_w, button_remove_w, path_chooser_w]

#Function called when the value of choose_w is changed
def on_change(change):
    if change['name']=='value':
        choose_action()

#Function called when the button is pressed to add link or protein displays another warning
def on_click_warning(click):
    global mygraph
    global message
    success=True
    if choice_w.value==3:
        rm_p=mygraph.find_protein(dropdown_proteins.value)
        if rm_p==None:
            message=("\033[91mProtein "+str(dropdown_proteins.value)+" not in proteins list.\033[0m")
            success=False
            #choose_action()
        else:
            print("Are you sure you want to delete protein "+str(dropdown_proteins.value)+"?")
            link_list=mygraph.find_links(rm_p)
            if len(link_list)!=0:
                print("Removing it will cause also the removal of the following links:")
                for l in link_list:
                    print("\t"+str(l))
    elif choice_w.value==4:
        #Here proteins must exists since it's a dropdown choice
        rm_p1=mygraph.find_protein(text_p1_link.value)
        rm_p2=mygraph.find_protein(text_p2_link.value)
        if mygraph.find_link(rm_p1, rm_p2)==None:
            message=("\033[91mLink from "+str(rm_p1)+" to "+str(rm_p2)+" not in links list.\033[0m")
            success=False
            #choose_action()
        else:
            print("Are you sure you want to delete the link between "+str(rm_p1)+" and "+str(rm_p2)+"?")
    if success:
        items = [widgets.Button(description="Yes"), widgets.Button(description="No")]
        items[0].on_click(yes_remove_click)
        items[1].on_click(no_remove_click)
        display(widgets.Box(items))
    else:
        choose_action()
        
#Function called when the button is pressed to add link or protein
def on_click(click):
    global mygraph
    global message
    if choice_w.value==1:
        new_p=Protein(_id=len(mygraph.proteins), _name=text_p_name.value, _color=color_w.value, _description=text_description.value)
        (nxG, pL)=mygraph.add_protein(new_p)
        if nxG==None and pL==None:
            message=("\033[91mProtein "+new_p.name+" already in list.\033[0m")
        else:
            message=("\033[94mProtein "+new_p.name+" added.\033[0m")
        #clean widget
        text_p_name.value=""
        color_w.value="#000000"
        text_description.value=""
        
        choose_action()
    if choice_w.value==2:
        P1=mygraph.find_protein(text_p1_link.value)
        P2=mygraph.find_protein(text_p2_link.value)
        if P1==None or P2==None:
            if P1==None:
                message=("\033[91mProtein "+text_p1_link.value+" does not exist, cannot create link from "+text_p1_link.value+" to "+text_p2_link.value+".\033[0m")
            if P2==None:
                message=("\033[91mProtein "+text_p2_link.value+" does not exist, cannot create link from "+text_p1_link.value+" to "+text_p2_link.value+".\033[0m")
        else:
            new_l=Link(_p1=P1, _p2=P2, _description=text_description.value, _color=color_w.value)
            nxG, lL=mygraph.add_link(new_l)
            if nxG==None and lL==None:
                message=("\033[91mLink from "+str(new_l.p1)+" to "+str(new_l.p2)+" already in list.\033[0m")
            else:
                message=("\033[94mLink from "+str(new_l.p1)+" to "+str(new_l.p2)+" added.\033[0m")
        #clean widget
        color_w.value="#000000"
        text_description.value=""
        
        choose_action()
    if choice_w.value==3:
        pass

def yes_remove_click(click):
    global mygraph
    if choice_w.value==3:
        mygraph.remove_protein(dropdown_proteins.value)
    elif choice_w.value==4:
        output=mygraph.remove_link_with_ps(text_p1_link.value, text_p2_link.value)
    choose_action()
            
def no_remove_click(click):
    choose_action()

def updateHVDisplay(value):
    global hvGrahDisplay
    hvGrahDisplay.update(value)

def saveGraph(chooser):
    mygraph.hvGraphSave(chooser.selected_path+"image.png")

choice_w.observe(on_change)
button_w.on_click(on_click)
button_remove_w.on_click(on_click_warning)
path_chooser_w.register_callback(saveGraph)

def choose_action(clear=True, resetValue=False):
    global mygraph
    global message
    global justOpened
    
    if resetValue:
        choice_w.value=1
    
    if clear:
        clear_output()
    if justOpened:
        print("Using graph: "+mygraph.name)
        justOpened=False
    if message!="":
        print(message)
        message=""
    print("Choose what to do: ")
    display(choice_w)
    choice=choice_w.value
    if choice in [1, 2]: #Add protein or link
        if choice==1:
            print("Insert the data for the new protein:")
            display(text_p_name)
        else:
            print("Insert the data for the new link:")
            text_p1_link.options=sorted(mygraph.proteins)
            text_p2_link.options=sorted(mygraph.proteins)
            display(text_p1_link)
            display(text_p2_link)
        display(color_w)
        display(text_description)
        display(button_w)
    elif choice in [3, 4]: #Remove protein or link
        if choice==3:
            print("Insert the name of the protein to remove:")
            dropdown_proteins.options=sorted(mygraph.proteins)
            display(dropdown_proteins)            
        else:
            print("Insert the name of the proteins ad the edges of the link:")
            text_p1_link.options=sorted(mygraph.proteins)
            text_p2_link.options=sorted(mygraph.proteins)
            display(text_p1_link)
            display(text_p2_link)
        display(button_remove_w)
    elif choice in [5, 6, 7]: #List elements
        if choice==5: #List the proteins with their links
            if len(mygraph.proteins)==0:
                print([])
            else:
                for p in sorted(mygraph.proteins):
                    print(str(p))
                    link_list=mygraph.find_links(mygraph.find_protein(p))
                    for l in link_list:
                        print("\t"+str(l))
                    print()
        elif choice==6: #List the links
            for lid in range(len(mygraph.links)):
                print(str(mygraph.links[lid]), end="")
                if lid!=len(mygraph.links)-1:
                    print(end=", ")
                else:
                    print()
        elif choice==7: #List the proteins and the links
            proteins_s=""
            for p in mygraph.proteins:
                proteins_s+=str(p)+"\n"
            links_s=""
            for l in mygraph.links:
                links_s+=str(l)+"\n"
            display(widgets.Box([widgets.Textarea(value=proteins_s), widgets.Textarea(value=links_s)]))   
    elif choice==8: #Update Holoviews
        updateHVDisplay(mygraph.hvGraph())
    elif choice==9: #Save Holoviews
        display(path_chooser_w)
    mygraph.write_graph()
