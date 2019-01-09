#from random import randint
import pyorient
import sys
import time
from py2neo import Graph, Node, Relationship
import matplotlib.pyplot as plt
import os
import psutil
if __name__ == "__main__":
    #create connection 
    client = pyorient.OrientDB("localhost", 2424) 
    session_id = client.connect( "root", "3386" )
    #print(sys.argv[1])
    #create a database 
    db_name = "insert"+ sys.argv[1]
    db_username = "admin"
    db_password = "admin"

    if client.db_exists(db_name):
        #print("dropping...")
        client.db_drop(db_name)
        
    #print("begin create")
    client.db_create(db_name, pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_PLOCAL)
    print("create succesfully")

    client.db_open( db_name, db_username, db_password )



    #create V 
    
    
    orient_vinsert = []
    cpu_usage = []
    ram_usage = []
    disk_usage = []
    #print("total vertex: " + str(int(sys.argv[1])))
    pid = os.getpid()
    py = psutil.Process(pid)
    initram =  py.memory_info()[0]/2.**30
    v_start = time.time()
    for v_num in range( int(sys.argv[1])):
        #client.command('delete vertex V')
        #print("total vertex insert: "+ str(v_num))
        #v_start = time.time()
        

        rec = { '@V': { 'name': v_num  } }
        rec_position = client.record_create( 11, rec )#17: cluster id of student --> pyorient bug!!
        cpu_usage.append(py.cpu_percent(interval=0))
        memoryUse = py.memory_info()[0]/2.**30
        ram_usage.append(memoryUse-initram)
        disk_usage.append(psutil.disk_usage('/').percent)

        #collect time
        ####################################################
        if v_num%1000 == 0 and v_num!=0:
            v_total = time.time() - v_start
            orient_vinsert.append(v_total)
            #v_start = time.time()

        ##########################################################

    print("orient_vtime = " ,orient_vinsert)
    print("orient_vram_usage = ",ram_usage)
    print("orient_vcpu_usage = ",cpu_usage)
    print("orient_vdisk_usage = " , disk_usage)
   
    #plt.plot(x , orient_vinsert)
   
    #create E
    x = [i for i  in range(1000 , int(sys.argv[1])+1 , 1000) ]
    plt.subplot(2,2,1)
    plt.plot(x, orient_vinsert)
    x = [i for i  in range( int(sys.argv[1])) ]
    plt.subplot(2,2,2)
    plt.plot(x, cpu_usage)
    plt.subplot(2,2,3)
    plt.plot(x, ram_usage)
    plt.subplot(2,2,4)
    plt.plot(x, disk_usage)
    plt.show()
    """
    E = { i :[] for i in range(int(sys.argv[1]))}
    """
    #print(E)
    #create edge
    
    

client.db_close()
