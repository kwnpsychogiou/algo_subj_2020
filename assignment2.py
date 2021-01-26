def basedOnLinks(x, L):#x: to nn dld poses fores tha epanalavw thn didikasia L: adjacency list 
    
    for a in range(x):
        max = -1
        for i in L:
            if len(L[i]) > max:
                max = len(L[i])
                komvos = i #vrhka oti o komvos i exei perisoterous geitones apo to max
            elif (len(L[i]) == max):
                if (i < komvos):
                    komvos = i
        print(komvos, len(L[komvos]))
        for i in L[komvos]: #gia kathe geitona tou komvou pou vrhka
            L[i].remove(komvos) #thelw na diagrapsw apo thn lista kathe geitona tou komvou(me to megalithero vathmo) ton komvo auton 
        del [L[komvos]]
    
def ball(G, node, r, perimeter=False):
    
    q = deque()
    neighbors = {}
    visited =  [ False ] * (len(G) + 1) 
    inqueue =  [ False ] * (len(G) + 1) 
    q.appendleft(node)
    inqueue[node] = True
    rad = 0
    for x in range(r+2):
        neighbors[x] = []
    while len(q) != 0 and rad <= r:         
        c = q.pop()
        inqueue[c] = False
        visited[c] = True
        if (c in neighbors[rad+1]):
            rad += 1
        if rad > r:
            break
        if (c not in neighbors[rad]):
            neighbors[rad].append(c)
              
        for v in G[c]:
            if not visited[v] and not inqueue[v]:
                q.appendleft(v)
                inqueue[v] = True
                neighbors[(rad+1)].append(v)
    if (perimeter):
        return neighbors[r]
    return neighbors

def basedOnCI(G, x, r): #x: num of nodes r: aktina

    CI = {}
    neighbors = {}
    allneighbors = {}
    for v in G.keys():
        ci = 0
        listofneighb = ball(G, v, r)
        neighbors[v] = listofneighb[r] #to θball(v,r)
        allneighbors[v] = [a for i in listofneighb.keys() if i != 0 for a in listofneighb[i]] #to ball(v,r+1)
        for a in neighbors[v]:
            ci += (len(G[a]) - 1)
        CI[v] =  (len(G[v]) - 1) * ci
    removednodes=[]
    for i in range(x):
        max = -1
        for v in CI.keys():
            if CI[v] > max:
                max = CI[v]
                komvos = v
            elif CI[v] == max:
                if komvos > v:
                    komvos = v
        print(komvos, max)
        for i in G[komvos]: #gia kathe geitona tou komvou pou vrhka
            G[i].remove(komvos) #thelw na diagrapsw apo thn lista kathe geitona tou komvou(me to megalithero vathmo) ton komvo auton 
        removednodes.append(komvos)
        G[komvos] = [] 
        del CI[komvos]

        for i in allneighbors[komvos]:
            changing_neighb = ball(G,i,r, True)
            ci = 0
            for v in changing_neighb: 
                if v not in removednodes:
                    ci += (len(G[v]) - 1)
            CI[i] =  (len(G[i]) - 1) * ci 
    
        
from collections import deque 
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-c", action="store_true") #an dwsei -c xrhsimopoiw tous sindesmous kathe node
parser.add_argument("-r ", "--RADIUS", type=int, help="insert the radius")
parser.add_argument("num_nodes", type=int, help="the number of nodes you want to be removed")
parser.add_argument("filename", help="the filename")
args = parser.parse_args()
nn = args.num_nodes
adjList = {}
with open(args.filename) as f:
    for line in f:
        nodes = [int(x) for x in line.split()]
        if nodes[0] not in adjList:
            adjList[nodes[0]] = []
        if nodes[1] not in adjList:
            adjList[nodes[1]] = []
        adjList[nodes[0]].append(nodes[1]) #enhmerwnw thn lista geitniashs vazontas ton deksi komvo
        adjList[nodes[1]].append(nodes[0]) # "" vazontas ton aristero komvo giati to arxeio periexei apla to poioi komvoi einai sindedemenoi
f.close()
if (args.c):
    basedOnLinks(nn, adjList)
else:
    basedOnCI(adjList, nn, args.RADIUS)


