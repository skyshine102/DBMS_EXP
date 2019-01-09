from random import randint
import pyorient
import numpy as np
import sys
import os
import psutil
import time
from py2neo import Graph, Node, Relationship
import matplotlib.pyplot as plt
 
if __name__ == "__main__":
    #create connection 
    client = pyorient.OrientDB("localhost", 2424) 
    session_id = client.connect( "root", "1234" )
    #print(sys.argv[1])
    #create a database 
    db_name = "insertE"+ sys.argv[1]
    db_username = "admin"
    db_password = "admin"
    pid = os.getpid()
    py = psutil.Process(pid)
    if client.db_exists(db_name):
        print("dropping...")
        client.db_drop(db_name)
        
    print("begin create")
    client.db_create(db_name, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_PLOCAL)
    print("create succesfully")

    try :
        client.db_open( db_name, db_username, db_password )
        #print(db_name + " opened successfully")
    except:
        print(db_name + " opened failed")
        sys.exit()


    client.command('delete vertex V')
    v_id_map = {}
    print("create 1000 nodes...")
    for i in range(1000):
        rec = { '@V': { 'name': i  } }
        rec_position = client.record_create( 11, rec )#17: cluster id of student --> pyorient bug!!
        v_id_map[i] = rec_position


    orient_Einsert = []
    cpu_usage = []
    ram_usage = []
    disk_usage = []
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
    initdisk = psutil.disk_usage('/').percent
    initram =  py.memory_info()[0]/2.**30
    for k,v in E.items():
        for e2 in v:
            E_start = time.time()
            edgecmd = "create edge E from " + v_id_map[k]._rid + " to " +v_id_map[e2]._rid
            res = client.command( edgecmd )
            E_time += time.time() - E_start
            cpu_usage.append(py.cpu_percent(interval=0))
            memoryUse = py.memory_info()[0]/2.**30
            ram_usage.append(memoryUse-initram)
            disk_usage.append(psutil.disk_usage('/').percent-initdisk)
            
            edge_count += 1
            if edge_count%1000 == 0:
                orient_Einsert.append(E_time)
    #v_total = time.time() - v_start
    if edge_count != E_num*1000:
        orient_Einsert.append(E_time)
        

    print("orient_einsert = " , orient_Einsert)
    print("ram_eusage = ",ram_usage)
    print("cpu_eusage = ",cpu_usage)
    print("disk_eusage = " , disk_usage)

    x = [i for i  in range(1000 , int(sys.argv[1])*1000+1 , 1000) ]
    plt.subplot(2,2,1)
    plt.plot(x, orient_Einsert)
    x = [i for i  in range(edge_count) ]
    plt.subplot(2,2,2)
    plt.plot(x, cpu_usage)
    plt.subplot(2,2,3)
    plt.plot(x, ram_usage)
    plt.subplot(2,2,4)
    plt.plot(x, disk_usage)
    plt.show()


    """
    
    """
    #print(E)
    #create edge
    
    

client.db_close()
