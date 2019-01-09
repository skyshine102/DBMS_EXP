orient_traverse =  [0.1877613067626953, 0.24021553993225098, 0.27409934997558594, 0.3578057289123535, 0.4563729763031006, 0.4930613040924072, 0.5274159908294678, 0.6202824115753174, 0.6881144046783447, 0.7181031703948975]
orient_ram_triusage =  [0.00196075439453125, 0.002285003662109375, 0.003345489501953125, 0.00395965576171875, 0.005401611328125, 0.005016326904296875, 0.006244659423828125, 0.00879669189453125, 0.0098114013671875, 0.009674072265625]
orient_cpu_triusage =  [0.0, 42.7, 48.0, 52.2, 57.3, 55.0, 59.2, 61.8, 64.0, 63.9]
orient_disk_triusage =  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

neo_traverse =  [0.043506622314453125, 0.04935741424560547, 0.038820505142211914, 0.05626726150512695, 0.03867745399475098, 0.03424882888793945, 0.03358626365661621, 0.08788061141967773, 0.036386966705322266, 0.027562856674194336]
neo_ram_triusage =  [0.0009765625, 0.000492095947265625, -3.814697265625e-06, 3.814697265625e-06, 0.000247955322265625, 0.0, 0.0, 0.0, 0.0, 0.0]
neo_cpu_triusage =  [0.0, 15.1, 15.1, 16.3, 14.4, 14.0, 14.9, 17.1, 15.2, 18.3]
neo_disk_triusage =  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
import matplotlib.pyplot as plt
x = [i for i  in range(1000 , 10001 , 1000) ]
ax = plt.subplot(2,2,1)
ax.plot(x, orient_traverse , c ='k' , label  = 'orientDB')
ax.plot(x,neo_traverse , c = 'b',label  = 'neo4j')
x1 = [i for i  in range(1000 , 10001 , 1000) ]
x2 = [ i for i  in range(1000 , 10001 , 1000)]
x = [i for i  in range(10000) ]
ax1 = plt.subplot(2,2,2)
ax1.plot(x1, orient_cpu_triusage , c = 'k' ,label  = 'orientDB')
ax1.plot(x2, neo_cpu_triusage, c = 'b', label  = 'neo4j')
ax2 = plt.subplot(2,2,3)
ax2.plot(x1, orient_ram_triusage , c = 'k', label  = 'orientDB')
ax2.plot(x2 , neo_ram_triusage , c = 'b',label  = 'neo4j')
ax3=plt.subplot(2,2,4)
ax3.plot(x1, orient_disk_triusage , c = 'k', label  = 'orientDB')
ax3.plot(x2 , neo_disk_triusage , c = 'b',label  = 'neo4j')

plt.suptitle("traverse to 10000 edges" , fontsize = 32)
ax.set_title("traverse time", fontsize = 22)
ax.set_ylabel("time(s)", fontsize = 20)
ax.xaxis.set_tick_params(labelsize=16)
ax.yaxis.set_tick_params(labelsize=16)
#ax.set_xlabel("# of nodes")

#ax1.set_xlabel("# of nodes")
ax1.set_title("cpu consumption", fontsize = 22)
ax1.set_ylabel("cpu consumption(%)", fontsize = 22)
ax1.xaxis.set_tick_params(labelsize=16)
ax1.yaxis.set_tick_params(labelsize=16)

ax2.set_xlabel("# of edges", fontsize = 22)
ax2.set_title("memory consumption", fontsize = 22)
ax2.set_ylabel("memory consumption(GB)", fontsize = 22)
ax2.xaxis.set_tick_params(labelsize=16)
ax2.yaxis.set_tick_params(labelsize=16)

ax3.set_xlabel("# of edges", fontsize = 22)
ax3.set_title("disk space used", fontsize = 22)
ax3.set_ylabel("used space(%)", fontsize = 22)
ax3.xaxis.set_tick_params(labelsize=16)
ax3.yaxis.set_tick_params(labelsize=16)
plt.legend(loc = 'best',fontsize = 22)
plt.show()