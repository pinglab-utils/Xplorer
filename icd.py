from flask import Flask, request,render_template
import networkx as nx
import json as json
import random as random
import matplotlib.pyplot as plt
import os
from flask import g, Response


app = Flask(__name__)


'''Welcome Page'''
@app.route("/")
def welcome():
    return render_template('index.html')

#============= Trst graph ========================

'''test '''
@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/test_data')
def test_data():
    with open('data/test.json', 'r') as f:
        test_data = json.load(f)
        
    nodes = test_data['nodes']
    links = test_data['links']
    
    return  Response(json.dumps({"nodes": nodes, "links": links}),
                    mimetype="application/json") 

'''tree '''
@app.route('/tree')
def tree():
    return render_template('tree.html')

#================= Ask single Node =====================

'''Ask single node '''
@app.route('/ask_one')
def ask_one():
    return render_template('ask_one.html')


'''Reply single node info'''
@app.route("/result_one",methods = ['POST', 'GET'])
def result_one():
    if request.method == 'POST':
        result = request.form
        global G
        info = {}
        ROOT = "ICD11"
        source_node = result["source"]
        root_source = nx.shortest_path(G,source=ROOT,target=source_node)[1]
        source_neighbours = G.neighbors(source_node)
        
        NBD = []
        for item in source_neighbours:
            
            NBD.append({"id":item,\
                        "title":G.nodes()[item]['title'],\
                        "code" : G.nodes()[item]['code']})
        
        path = nx.shortest_path(G, ROOT, source_node)
        
        PATH_NAMES = []
        for item in path:
            PATH_NAMES.append({"id":item,\
                               "title":G.nodes()[item]['title'],\
                               "code" : G.nodes()[item]['code']})
        
        
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


        return render_template("result_one.html", info = info)
    
    
# =============== Two node relation ==============================    
    
    
'''ask two node relation'''    
@app.route('/boot_ask_two')
def boot_ask_two():
    return render_template('boot_ask_two.html')

@app.route("/boot_result_two",methods = ['POST', 'GET'])
def boot_result_two():
    if request.method == 'POST':
        result = request.form
        global G
        info = {}
        ROOT = "ICD11"
        common_child = True
        source_node = result["source"]
        target_node = result["target"]
        
        root_source = nx.shortest_path(G,source=ROOT,target=source_node)[1]
        root_target = nx.shortest_path(G,source=ROOT,target=target_node)[1]
        
        
        path = nx.shortest_path(G, source_node, target_node)
        if "ICD11" in path:
            common_child == False

        SG = nx.Graph()
        for node in path:
            nbd = [n for n in G.neighbors(node)]
            SG.add_node(node)
            for item in nbd:
                SG.add_node(item)
            for item in nbd:
                SG.add_edge(node,item)

        info.update({"path":path,\
                "source":source_node,\
                "target":target_node,\
                "source_root":root_source,\
                "target_root":root_target,\
                "path_length": len(path),\
                "common_child": common_child,\
                "info":nx.info(SG),\
                "nodes":SG.nodes()})


        return render_template("boot_result_two.html", info = info)
    
    
#================ Part Visual ============================   

@app.route('/visual')
def visual():
    return render_template('visual.html')

@app.route("/graph")
def get_graph():
    SG = nx.Graph()
    nodes = []
    links = []
    n1 = '1307379503'
    n2 = '1369242951'
    path = nx.shortest_path(G,source=n1,target=n2)
    for node in path:
        nbd = [n for n in G.neighbors(node)]
        
        nodes.append({"title": node,\
                      "group":str(random.choice([1,2,3,4])),\
                      "color":random.choice(["red","blue","green"])})
        
        for item in nbd:
            nodes.append({"title": item,\
                          "group":str(random.choice([1,2,3,4])),\
                          "color":random.choice(["red","blue","green"])})
            
            links.append({"source": node,\
                         "target": item,\
                         "value":random.choice([1,2,3,4])})
                
           
    return Response(json.dumps({"nodes": nodes, "links": links}),
                    mimetype="application/json") 
    
    
   


#=================== Supportive Functions  ====================================

@app.route("/path")
def path():
    global G
    info = {}
    source = '1307379503'
    target = '1369242951'

    path = nx.shortest_path(G, source, target)

    info.update({"source":source,\
                "target":target,\
                "path":path,\
                "path_length":len(path)})

    return render_template("path.html", info = info)


@app.route("/subgraph")
def subgraph():
    SG = nx.Graph()
    info = {}
    source = '1307379503'
    target = '1369242951'
    SG = nx.Graph()
    path = nx.shortest_path(G, source, target)
    for node in path:
        nbd = [n for n in G.neighbors(node)]
        SG.add_node(node)
        for item in nbd:
            SG.add_node(item)
        for item in nbd:
            SG.add_edge(node,item)

    info.update({"path":path,\
                "source":source,\
                "target":target,\
                "path_length": len(path),\
                "info":nx.info(SG),\
                "nodes":SG.nodes()})


    return render_template("subgraph.html", info = info)

@app.route("/boot_ask_one")
def boot():
    global G
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
        root_source = nx.shortest_path(G,source=ROOT,target=source_node)[1]
        source_neighbours = G.neighbors(source_node)
        
        NBD = []
        for item in source_neighbours:
            
            NBD.append({"id":item,\
                        "title":G.nodes()[item]['title'],\
                        "code" : G.nodes()[item]['code']})
        
        path = nx.shortest_path(G, ROOT, source_node)
        
        PATH_NAMES = []
        for item in path:
            PATH_NAMES.append({"id":item,\
                               "title":G.nodes()[item]['title'],\
                               "code" : G.nodes()[item]['code']})
        
        
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
    



@app.route("/tree_data")
def tree_data():
    SG = nx.Graph()
    info = {}
    source_node = '1307379503'
    ROOT = "ICD11"
    nodes = []
    links = []
    
    SG = nx.Graph()
    path = nx.shortest_path(G, source=ROOT, target=source_node)
    
    
    i = 0
    for node in path:
        i = i+1
        node_dict = {"name": str(node),\
                      "group":random.choice([1,2,3,4]),\
                      "sn": i}
        
        nodes.append({"name" : node_dict["name"],\
                      "group": node_dict["group"]})
        
 
        nbd = [n for n in G.neighbors(node)]
    
        for item in nbd:
            if item not in path:
                i = i+1
                item_dict = {"name": str(item),\
                         "group":random.choice([1,2,3,4]),\
                         "sn" : i}
            
                nodes.append({"name" : item_dict["name"],\
                          "group": item_dict["group"]})
            
            
            
                links.append({"source": node_dict["sn"],\
                         "target": item_dict["sn"],\
                         "value":random.choice([1,2,3,4])})
                
           
    return Response(json.dumps({"nodes": nodes, "links": links}),
                    mimetype="application/json") 

 
#================== Run APplication ==========================
    
    
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
                   defn = item['defn'])
        except:
            G.add_node(item_id,\
                   title = "Key not found",\
                   code = item['code'],\
                   defn = item['defn'])  
        
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



