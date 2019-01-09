from random import randint
import pyorient
import numpy as np
import sys
import time
from py2neo import Graph, Node, Relationship
import matplotlib.pyplot as plt
import os
import psutil

uri = "bolt://localhost:7687"
user = "neo4j"
password = "1234"

graph = Graph(uri=uri, user=user, password=password)
pid = os.getpid()
py = psutil.Process(pid)

neo_Einsert = []
cpu_usage = []
ram_usage = []
disk_usage = []

#print("total vertex: " + str(int(sys.argv[1])))
graph.run("MATCH (n) DETACH DELETE n")
for i in range(1000):
    graph.run("MERGE (n:Node{id:{id}})", id = i)

print("1000 vertex created")
E_num = int(sys.argv[1])
print("total edge "+ str(E_num*1000))

print("costructing E...")
edge = list(np.random.randint(1000 , size = E_num*1000))
#print(edge)
E=dict()
for i in range(1000):
	#E_count = int(np.random.randint(1, 3*E_num , size = 1)[0]) 
	E_count = E_num
	if len(edge) >= E_count:
		E[i] = list(set([j for j in edge[:E_count]]))
		edge = edge[E_count:]
	else: #last piece
		E[i] = list(set([j for j in edge])) 
		edge = []      
#print(E)
E_id_map = {}
#v_start = time.time()
print('start creating and connecting E of '+ str(E_num*1000))
E_time = 0
edge_count = 0
initram =  py.memory_info()[0]/2.**30
initdisk =psutil.disk_usage('/').percent
for k,v in E.items():
	for e2 in v:
		E_start = time.time()
		graph.run("MATCH (m:Node{id:{id1}}),(n:Node{id:{id2}}) CREATE (m)-[:Edge]->(n)",id1 = int(k), id2 = int(e2))
		cpu_usage.append(py.cpu_percent(interval=0))
		E_time += time.time() - E_start
		memoryUse = py.memory_info()[0]/2.**30
		ram_usage.append(memoryUse-initram)
		disk_usage.append(psutil.disk_usage('/').percent-initdisk)
		edge_count += 1
		if edge_count%1000 == 0:
			neo_Einsert.append(E_time)
if edge_count != E_num*1000:
	neo_Einsert.append(E_time)
print("neo_einsert = " , neo_Einsert)
print("neo_ram_eusage = ",ram_usage)
print("neo_cpu_eusage = ",cpu_usage)
print("neo_disk_eusage = " , disk_usage)

x = [i for i  in range(1000 , int(sys.argv[1])*1000+1 , 1000) ]
plt.subplot(2,2,1)
plt.plot(x, neo_Einsert)
x = [i for i  in range(edge_count) ]
plt.subplot(2,2,2)
plt.plot(x, cpu_usage)
plt.subplot(2,2,3)
plt.plot(x, ram_usage)
plt.subplot(2,2,4)
plt.plot(x, disk_usage)
plt.show()
