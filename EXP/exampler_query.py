from py2neo import Graph, Node, Relationship
import sys
import csv
import itertools
from collections import Counter
import time
import operator
import logging
import jieba
from gensim import models
from gensim.models import word2vec
import warnings
warnings.filterwarnings(action='ignore',category=UserWarning,module='gensim')
#from gensim.models import word2vec

start_time = time.time()
def cut_edge(a):
    temp = a
    a1 = 0
    a2 = 0
    for i in range(len(a)-1):
        if a[i:i+2] == "[:":
            a1 = i+1
        if a[i:i+2] == " {":
            a2 = i
    return temp[a1+1:a2]
input_query = input("=== seperate words by space \n=== add -s at the end for sorting result by semantic===  \n=== type quit to exit program \ninput your query : ")
while input_query != "quit":
    temp_input = input_query.split()
    op = 2
    input_list = []
    for i in range(len(temp_input)):
        if temp_input[i] == "-s":
            op = 1
        else:
            input_list.append(temp_input[i].replace("_", " "))
            
    if op == 1:
        #logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        model = models.Word2Vec.load('word2vec.model')
        jieba.set_dictionary('jieba_dict/dict.txt.big')


    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "rigo1205"#should be change to your own password
    graph = Graph(uri=uri, user=user, password=password)

    in_len = len(input_list)
    if(len(input_list) == 1):
        node_list = []
        edge = []
        temp_n = graph.run("MATCH (p {name:{p1}})-[n]-(q) RETURN COUNT(n) AS count_edge, type(n) ORDER BY type(n) DESC", p1=input_list[0])
        t = list(temp_n)
        dictionary1 = {t[i][1]:t[i][0] for i in range(len(t))}
        summ = sum(dictionary1.values())
        nodes = list(graph.run("MATCH (p) RETURN p.name LIMIT 1000"))   
        nodes = [nodes[i][0] for i in range(len(nodes))]
        for node in nodes:
            query = list(graph.run("MATCH (p {name:{p1}})-[n]-(q) RETURN COUNT(n) AS count_edge, type(n) ORDER BY type(n) DESC", p1=node))
            dictionary2 = {query[i][1]:query[i][0] for i in range(len(query))} 
            if dictionary1 == dictionary2:
                node_list.append(node)
        for i in node_list:
            print(i)
        end_time = start_time - time.time()
        
    else:
        Match = []
        for i in range(in_len-1):
            temp_n = graph.run("MATCH(p) WHERE p.name={p1} RETURN p", p1=input_list[i])
        sample_nodes = set()
        sample_edges = []
        for i in range(len(input_list) - 1):
            for j in range(i+1,len(input_list)):
                a = graph.run("MATCH p1= shortestPath((p)-[*]-(r)) WHERE p.name = {name1} AND r.name = {name2} RETURN p1 LIMIT 100", name1 = input_list[i], name2 = input_list[j])
                q1 = list(a)
                temp2 = set()
                for record in q1:
                    node = record["p1"].nodes
                    edge = record["p1"].relationships
                    temp = []
                    for re in edge:
                        temp.append(cut_edge(str(re)))
                    temp2.add(tuple(temp))
                sample_edges.append(list(temp2))
        query = []
        start = 1
        end = 2
        end2 = 2
        thresh = len(input_list)-1
        thresh2 = len(input_list)-1
        for i in range(1,len(sample_edges)+1):
            temp2 = []
            for j in range(len(sample_edges[i-1])):
                temp = "MATCH (r"+str(start)+")-"
                for k in range(len(sample_edges[i-1][j])):
                    if k != len(sample_edges[i-1][j])-1:
                        temp = temp +"[:"+sample_edges[i-1][j][k]+"]-(g"+str(i-1)+str(j)+str(k)+")-"
                    else:
                        temp = temp +"[:"+sample_edges[i-1][j][k]+"]-"
                temp = temp + "(r"+str(end)+")"
                temp2.append(temp)
            query.append(temp2)
            if i == thresh:
                start = start + 1
                thresh2 = thresh2 - 1
                thresh = thresh2 + i
                end2 = end2 + 1
                end = end2
            else:
                end = end + 1
        structure_query=[]
        iter_query = list(itertools.product(*query))
        length = 0
        for i in range(len(input_list)):
            length = length+i
        for qu in iter_query:
            temp_q = '' 
            for i in range(length):
                temp_q = temp_q + qu[i] + " \n"
            temp_q = temp_q + "RETURN "
            for i in range(len(input_list)):
                temp_q = temp_q + "r" + str(i+1) + ", "
            temp_q = temp_q[:-2]
            temp_q = temp_q + " \n"
            temp_q = temp_q + "LIMIT 100"
            structure_query.append(temp_q)
        if op == 1:
            ans_node = set()
            ans_dict = {}
            for st in range(len(structure_query)):
                ans = graph.run(structure_query[st])
                ans_l = list(ans)
                for temp_a in ans_l:
                    temp = []
                    score = 0
                    index = 0
                    for i in temp_a:
                        temp.append(i["name"])
                        if input_list[index] != i["name"]:
                            ph1 = jieba.cut(input_list[index], cut_all=True)
                            ph2 = jieba.cut(i["name"], cut_all=True)
                            ph1_l = []
                            ph2_l = []
                            for i in ph1:
                                ph1_l.append(i)
                            for i in ph2:
                                ph2_l.append(i)
                            temp_score = 0            
                            for i in range(len(ph1_l)):
                                
                                
                                for j in range(len(ph2_l)):
                                    num = 0
                                    boolean = 0
                                    try : 
                                        semi = model.most_similar(ph1_l[i] , topn = 1)
                                        semi2 = model.most_similar(ph2_l[j] , topn = 1)
                                    except KeyError:
                                        boolean = 1
                                        res = 0
                                    if boolean == 0:
                                        res = model.similarity(ph1_l[i],ph2_l[j])
                                        
                                    if res > num:
                                        num = res
                                temp_score = temp_score + num
                            temp_score = temp_score / len(ph1_l)
                            score = score + temp_score
                        else:
                            score = score + 1
                        score = score / len(input_list)    
                        index = index + 1 
                    ans_node.add(tuple(temp))
                    ans_dict[tuple(temp)] = score
            if tuple(input_list) in ans_dict:
                del ans_dict[tuple(input_list)]
            new_dict = sorted(ans_dict.items(), key=operator.itemgetter(1))
            new_dict = new_dict[::-1]
            count = 0
            for keys, values in new_dict:
                print(keys, values)
                count = count + 1
                if count == 100:
                    break
        if op == 2:
            ans_node = set()
            ans_dict = {}

            for st in range(len(structure_query)):
                ans = graph.run(structure_query[st])
                ans_l = list(ans)
                for temp_a in ans_l:
                    temp = []
                    score = 0
                    index = 0
                    for i in temp_a:
                        temp.append(i["name"])
                        if input_list[index] != i["name"]:            
                            path = list(graph.run("match(n1),(n2),p=shortestPath((n1)-[*]-(n2)) where n1.name = {name1} and n2.name = {name2} return length(p)", name1=input_list[index], name2=i["name"]))
                            length2 = path[0][0]
                            s = len(list(path))
                            score = score + length2
                        index = index + 1
                    ans_node.add(tuple(temp))
                    ans_dict[tuple(temp)] = score
            if tuple(input_list) in ans_dict:
                del ans_dict[tuple(input_list)]
            new_dict = sorted(ans_dict.items(), key=operator.itemgetter(1))
            count = 0
            for keys, values in new_dict:
                print(keys, values)
                count = count + 1
                if count == 100:
                    break
    input_query = input("=== seperate words by space \n=== add -s at the end for sorting result by semantic \n=== type quit to exit program \ninput your query : ")
