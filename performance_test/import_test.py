from py2neo import Graph, Node, Relationship
import sys
import matplotlib.pyplot as plt
import time

uri = "bolt://localhost:7687"
user = "neo4j"
password = "3386"

graph = Graph(uri=uri, user=user, password=password)
neo_vinsert = []
#print("total vertex: " + str(int(sys.argv[1])))
for v_num in range(1000 , int(sys.argv[1])+1 , 1000):
    graph.run("MATCH (n:Node) DETACH DELETE n")
    print("total vertex insert: "+ str(v_num))
    v_start = time.time()
    for i in range(v_num):
        graph.run("CREATE (n:Node{id:{id}})", id = i)
    v_total = time.time() - v_start
    neo_vinsert.append(v_total)
print(neo_vinsert)

x = [i for i  in range(1000 , int(sys.argv[1])+1 , 1000) ]
plt.plot(x , neo_vinsert)
plt.show()