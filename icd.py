from flask import Flask, request,render_template
import networkx as nx
import json as json
import pandas as pd
import random as random
import matplotlib.pyplot as plt
import os
from flask import g, Response


app = Flask(__name__)


'''Welcome Page'''
@app.route("/")
def welcome():
    return render_template('index.html')

#================= Ask single Node =====================

@app.route("/boot_ask_one")
def boot():
    global G
    
    '''Info for root nodes'''
    ROOT = [n for n in G.neighbors("ICD11")]
    INFO = []
    for node in ROOT:
        try:
            INFO.append({"ID": node,\
                     "title": G.nodes()[node]["title"],\
                     "defn":  G.nodes()[node]['defn'],\
                     "child": len([n for n in G.neighbors(node)])})
        except:
            
             INFO.append({"ID": node,\
                     "title": "NA",\
                     "defn":"NA",\
                     "child": "NA"})
                
    return render_template("boot_ask_one.html", info = INFO) 




'''Reply single node info'''
@app.route("/boot_result_one",methods = ['POST', 'GET'])
def boot_result_one():
    if request.method == 'POST':
        result = request.form
        global G
        info = {}
        ROOT = "ICD11"
        source_node = result["source"]
        
        
        '''Prepare root info'''
        root_source = nx.shortest_path(G,source=ROOT,target=source_node)[1]
        
        
        '''Collect Nrighbour info'''
        source_neighbours = G.neighbors(source_node)
        NBD = []
        for item in source_neighbours:
            
            NBD.append({"id":item,\
                        "title":G.nodes()[item]['title'],\
                        "code" : G.nodes()[item]['code']})
            
            
            
        '''Collect Path Info'''
        path = nx.shortest_path(G, ROOT, source_node)
        
        PATH_NAMES = []
        for item in path:
            PATH_NAMES.append({"id":item,\
                               "title":G.nodes()[item]['title'],\
                               "code" : G.nodes()[item]['code']})
            
            
            
        
        '''Collect Subgraph info'''
        SG = nx.Graph()
        for node in path:
            SG.add_node(node,title = G.nodes()[node]['title'],\
                          defn = G.nodes()[node]['defn'],\
                          code = G.nodes()[node]['code'])
            
            nbd = [n for n in G.neighbors(node)]
            for item in nbd:
                try:
                    SG.add_node(item,title = G.nodes()[item]['title'],\
                          defn = G.nodes()[item]['defn'],\
                          code = G.nodes()[item]['code'])
                except:
                    SG.add_node(item,title = "Key not found",\
                          defn = "key not found",\
                          code = "key not found")
               
            for item in nbd:
                SG.add_edge(node,item)
                
                
                
                
                
        '''Collect info data to boardcast'''
        info.update({"path":path,\
                "source":source_node,\
                "source_title":SG.nodes()[source_node]['title'],\
                "source_defn":SG.nodes()[source_node]['defn'],\
                "source_nbd": NBD,\
                "path_length": len(path),\
                "path_names": PATH_NAMES,\
                "source_root": root_source,\
                "source_root_title":G.nodes()[root_source]['title'],\
                "source_root_defn":G.nodes()[root_source]['defn'],\
                "info":nx.info(SG),\
                "nodes":SG.nodes()})


        return render_template("boot_result_one.html", info = info)
    



    
    
# =============== Two node relation ==============================    
    
    
'''ask two node relation'''    
@app.route('/boot_ask_two')
def boot_ask_two():
    
    '''Info for root nodes'''
    ROOT = [n for n in G.neighbors("ICD11")]
    INFO = []
    for node in ROOT:
        try:
            INFO.append({"ID": node,\
                     "title": G.nodes()[node]["title"],\
                     "defn":  G.nodes()[node]['defn'],\
                     "child": len([n for n in G.neighbors(node)])})
        except:
            
             INFO.append({"ID": node,\
                     "title": "NA",\
                     "defn":"NA",\
                     "child": "NA"})
    
    return render_template('boot_ask_two.html', info = INFO)


'''reply two node relation'''
@app.route("/boot_result_two",methods = ['POST', 'GET'])
def boot_result_two():
    if request.method == 'POST':
        result = request.form
        global G
        info = {}
        ROOT = "ICD11"
        common_child = True
        
        '''identify source and target'''
        source_node = result["source"]
        target_node = result["target"]
        source_title = G.nodes()[source_node]['title']
        target_title = G.nodes()[target_node]['title']
        source_defn =  G.nodes()[source_node]['defn']
        target_defn =  G.nodes()[target_node]['defn']
        
        
        '''find neighbourhood info'''
        source_neighbours = G.neighbors(source_node)
        target_neighbours = G.neighbors(target_node)
        
        s_NBD = []
        for item in source_neighbours:
            s_NBD.append({"id":item,\
                        "title":G.nodes()[item]['title'],\
                        "code" : G.nodes()[item]['code']})
            
        t_NBD = []
        for item in target_neighbours:
            t_NBD.append({"id":item,\
                        "title":G.nodes()[item]['title'],\
                        "code" : G.nodes()[item]['code']})
            
            
            
            
        '''find root info'''
        source_root = nx.shortest_path(G,source=ROOT,target=source_node)[1]
        target_root = nx.shortest_path(G,source=ROOT,target=target_node)[1]
        source_root_title = G.nodes()[source_root]['title']
        target_root_title = G.nodes()[target_root]['title']
        source_root_defn =  G.nodes()[source_root]['defn']
        target_root_defn =  G.nodes()[target_root]['defn']
        
        
        
        '''Collect path items'''
        path = nx.shortest_path(G, source_node, target_node)
        if "ICD11" in path:
            common_child == False
            
        PATH_NAMES = []
        for item in path:
            PATH_NAMES.append({"id":item,\
                               "title":G.nodes()[item]['title'],\
                               "code" : G.nodes()[item]['code']})
            
            
        '''Find subgraph info'''
        SG = nx.Graph()
        for node in path:
            nbd = [n for n in G.neighbors(node)]
            SG.add_node(node)
            for item in nbd:
                SG.add_node(item)
            for item in nbd:
                SG.add_edge(node,item)
                
                
                
        '''collect data to boardcast'''
        info.update({
                "source":source_node,\
                "target":target_node,\
                "s_NBD": s_NBD,\
                "t_NBD": t_NBD,\
                "source_title": source_title,\
                "target_title": target_title,\
                "source_defn": source_defn,\
                "target_defn": target_defn,\
                "source_root":source_root,\
                "target_root":target_root,\
                "source_root_title": source_root_title,\
                "target_root_title": target_root_title,\
                "source_root_defn": source_root_defn,\
                "target_root_defn": target_root_defn,\
                "path":path,\
                "path_names":PATH_NAMES,\
                "path_length": len(path),\
                "common_child": common_child,\
                "info":nx.info(SG),\
                "nodes":SG.nodes()})


        return render_template("boot_result_two.html", info = info)
    
    

#================== Run Application ==========================
    
    
if __name__ == '__main__':
   
    global G
    G = nx.Graph()

    with open('data/DATA.json', 'r') as f1:
        DATA = json.load(f1)
        
    with open('data/ROOTS.json', 'r')as f2:
        ROOTS = json.load(f2)

    for item in DATA:
        item_id = item['id']
        try:
            G.add_node(item_id,\
                   title = item['title'],\
                   code = item['code'],\
                   defn = item['defn'],\
                   childs = item['childs'])
        except:
            G.add_node(item_id,\
                   title = "Key not found",\
                   code = item['code'],\
                   defn = item['defn'],\
                   childs = item['childs'])  
        
        childs = item['childs']
        if childs!= 'Key Not found':
            for c_id in childs:
                G.add_edge(item_id,c_id)
            
            
    G.add_node("ICD11",\
           title="International Disease CLassification",\
           defn = "International Disease CLassification",\
           code = "ICD11")

    for root in ROOTS:
        G.add_edge("ICD11",root)


    app.run(port = 3000, debug = True)



