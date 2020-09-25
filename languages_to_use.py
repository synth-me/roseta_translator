import textblob
from textblob import TextBlob
import importlib
import node_func
import json 
import pathlib
import os 


# those are the deafult nodes
#l_list_1 = {
    #'ko':getattr(node_func,'korean_node'),
    #'zh':getattr(node_func,'chinese_node'),
    #'ja':getattr(node_func,'japanese_node')
#}

# we use this as a function so that we can import it later to the shell 
def json_route(path):
    return path 

p = pathlib.Path(__file__).parent.absolute()
z = str(p).split('/')

z[0].replace("\\","//")
main_path = str(z[0]+str('/path.json'))

path_unique = json.load(open(main_path,encoding='utf-8'))

p = open(path_unique['path'])
j = json.load(p)

l_list = {}

for value in j :

    j_ = j[value].split('.')
    j_.remove('node_func')
    jf = ''.join(j_)

    l_list[value] = getattr(node_func,jf)

def update_json():

    # this part will load the json root file and recheck the difference between the main dictionary
    # and the json file, the differences found between them will be erased. To null the differences the json
    # will get less priority , which means that the main file will subscribe the json with the differences between them
    # for every change in the main file the json is updated with the new info
    f = open(path_unique['path'])
    j = json.load(f)

    for l in l_list:
        try:
            j_ = (j[l]).split('.')
            j_.remove('node_func')
            jn = ''.join(j_)
            if l_list[l].__name__ == jn:
                print('same')
                pass 
            else:
# there's a difference between the two files
# so that we rewrite the json file with this novelty  
                print('updating...')
                with open(path_unique['path']) as JsonFile:
                    root = json.load(JsonFile)
# we then update the version here , given privilege for the main file 
                root[l] = 'node_func.'+l_list[l].__name__               
                with open(path_unique['path'],'w') as JsonFile:
                    json.dump(root,JsonFile)

        except KeyError:
# here we check the element that is new as a whole 
            print('updating...')
            with open(path_unique['path']) as JsonFile:
                root = json.load(JsonFile)
# we then update the version here , given privilege for the main file 
            root[l] = 'node_func.'+l_list[l].__name__
            with open(path_unique['path'],'w') as JsonFile:
                json.dump(root,JsonFile)
            print('sucessfully updated')

    return 'sucessfully updated'

def retreat_json():
# here we will make the other way out from the update. Here the system will first check 
# the information in the json and then in the main file. Given that the json have less priority 
# if some info is found in json and not in the main file then the system should exclud it from the json
    f = open(path_unique['path'])
    j = json.load(f)
    try:
        for v in j :
            if v not in l_list:
                with open(path_unique['path']) as JsonFile:
                    root = json.load(JsonFile)
                root.pop(v)                            
                with open(path_unique['path'],'w') as JsonFile:
                    json.dump(root,JsonFile) 
    except:
        return 'error on retreating'

    return True 


def uninstall(node):
# this function is made to specfically unplug nodes from the main source
    try:
        if node in l_list:
            l_list.pop(node)
            retreat_json()
            return 'sucessfully deplugged node'
        else:
            return 'cannot deplug a non existent node'
    except:
        return 'deplugging failed recheck...'

def change_path(path):
    with open(main_path,encoding='utf-8') as JsonFile:
        path_r = json.load(JsonFile)
# we then update the version here , given privilege for the main file 
    
    path_r['path'] = path                 
    
    with open(main_path,'w',encoding='utf-8') as JsonFile:
        json.dump(path_r,JsonFile)

    return 'changed path'

def language_list(add_node=None):
# here we list the pairs of node's names and node's functions 
# for roseta_main api, it acess is when the argument add_node is None so that we just get the
# pure information and can evoke the node
# the shell, otherwise, uses add_node with a pair of name / function to be added 
    if add_node != None:
        if add_node[0] in l_list.keys():
            return 'language already in use'
        else:
          try:
              g = getattr(node_func,add_node[1])
              l_list[add_node[0]] = g 
              update_json()
              return 'sucessfully plugged'
          except:
              return 'plugging failed check again your directory or function spelling'  
    else:
        return l_list 