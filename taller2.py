#!/usr/bin/env python3
import sys
from scapy.all import *
from time import *
import operator 
responses = {}
lastValidHoop = -1
no_response = 0

for ttl in range(1,25):
    ips_of_this_Hoop = {}
    for i in range(30):  
        probe = IP(dst=sys.argv[1], ttl=ttl) / ICMP()
        t_i = time()
        ans = sr1(probe, verbose=False, timeout=0.8)
        t_f = time()
        rtt = (t_f - t_i)*1000
        if ans is not None:
                if ans.src not in ips_of_this_Hoop:
                    ips_of_this_Hoop [ans.src]=[1,rtt]
                else:
                    # Acumula los tiempos y la cantidad de apareciones
                    ips_of_this_Hoop[ans.src]=[ ips_of_this_Hoop[ans.src][0]+1,ips_of_this_Hoop[ans.src][1]+rtt]
                    
    if len(ips_of_this_Hoop) != 0:

        ipMasUsada = max(ips_of_this_Hoop.items(), key=operator.itemgetter(1))[0]
        
        if lastValidHoop == -1:
            drtt = 0
        else:
            drtt = (ips_of_this_Hoop[ipMasUsada][1]/ips_of_this_Hoop[ipMasUsada][0]) - responses[lastValidHoop][0][1]

        rttPromedio = (ips_of_this_Hoop[ipMasUsada][1]/ips_of_this_Hoop[ipMasUsada][0])    
        responses[ttl] = []
        responses[ttl].append((ipMasUsada,rttPromedio,drtt))
        print(ttl,responses[ttl] )
        lastValidHoop = ttl
    else:
        no_response+= 1

print("% saltos sin respuesta: ", no_response*100/ttl) 
              
