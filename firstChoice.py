##Functions to manage first selection

from ipywidgets import widgets
from IPython.display import display, clear_output
from os import listdir
from time import sleep
from os import write

from secondChoice import *

init_choice_w=widgets.Dropdown(options=[
    ("Create new graph", 1),
    ("Start from last graph", 2),
    ("Open graph", 3),
    ], value=2)
next_button_w=widgets.Button(description="Next", icon="check")
file_chooser_w=widgets.FileUpload()
error=""

def on_change_init(change):
    global error
    clear_output(wait=True)
    if error!="":
        print(error)
    display(init_choice_w)
    if init_choice_w.value==1:
        display(graph_title)
    elif init_choice_w.value==2:
        pass
    elif init_choice_w.value==3:
        display(file_chooser_w)
    display(next_button_w)
        
def on_click_next(click):
    global mygraph 
    global error
    graph_name=""
    succed=True
    if init_choice_w.value==1: #Create new graph
        graph_name=graph_title.value
        file_list=listdir("saved")
        if graph_name in file_list or (graph_name+".graphml") in file_list:
            error="\033[91mFile "+graph_name+" already present, please choose another name or open the file manually.\033[0m"
            succed=False
        else:
            mygraph=GraphLib(graph_name)
    elif init_choice_w.value==2: #Open last graph
        try:
            with open(".last") as f:
                graph_name=f.readline()
                error+=("graph_name: "+graph_name)
        except:
            error+="\033[91mNo last file present, please insert new name or manually choose file to open.\033[0m"
            succed=False
        if succed:
            mygraph=mygraph.open_graph(graph_name)
        
    elif init_choice_w.value==3: #Open chosen graph
        graph_name=""
        i=0
        for key in file_chooser_w.value: #Widget is broken so I have to so this loop..........
            if i==0:
                graph_name=key
                i+=1
        mygraph=mygraph.open_graph(graph_name)
    if succed:
        with open(".last", "w+") as f:
            f.write(graph_name)
        choose_action()
    else:
        first_menu()
    
init_choice_w.observe(on_change_init)
next_button_w.on_click(on_click_next)

def first_menu():
    on_change_init(None)
    


