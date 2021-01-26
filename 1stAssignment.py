def CreatingGraph(n):
    G = {}
    neighbors = []
    for x in range (2-n,n):
        for y in range (0,n):
            if ( abs(x)+abs(y) < n ) and not( y==0 and x<0 ): #prepei sum(sintetagmenes)<5 kai gia y=o na mhn exw x<0
                neighbors = [(x+1,y),(x,y+1),(x-1,y),(x,y-1)] #vazw olous tous pithanous geitones kai meta tous diagrafw
                for (a,b) in neighbors[:]:
                    if (( abs(a)+abs(b)>=n ) or ( b==0 and a<0 ) or (b<0)):
                        neighbors.remove((a,b))
                G[(x,y)] = neighbors[:]
    return G

def AreNotNeighbors(graph, a, b, x): #a=o geitonas upo eksetash b=to polyomino x=to teleytaio tuple tou polyomino
    for z in b:
        if z != x:
            if a in graph[z]:
                return False          
    return True

def CountPolyominos(G, untried, size, pol):
    while untried:
        u = untried.pop()
        pol.append(u)
        if (len(pol) == size):
            c.x += 1
        else:
            new_neighbors = set()
            for v in G[u]:
                if (v not in untried) and (v not in pol) and (AreNotNeighbors(G, v, pol, u)):
                    new_neighbors.add(v)      
            new_untried = untried | new_neighbors
            CountPolyominos(G, new_untried, size, pol)
        pol.remove(u)
    return c.x

class Counter:
    x = 0

import argparse, pprint
parser = argparse.ArgumentParser()
parser.add_argument("n", type=int, help="polyominos_size")
parser.add_argument("-p", "--pgraph", action="store_true")
args = parser.parse_args()  
size = args.n
G = CreatingGraph(size)
if args.pgraph:
    pprint.pprint(G)           
pol = []
c = Counter()
print(CountPolyominos(G, {(0,0)}, size, pol))
 



