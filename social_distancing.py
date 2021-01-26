def dx(m, n):
    return n[0] - m[0]

def dy(m, n):
    return n[1] - m[1]

def distanceOf2Circles(m, n):
    d = math.sqrt(dx(m, n)**2 + dy(m, n)**2)
    return d

def distanceof2Circles(m, cix, ciy):
    dx = cix - m[0]
    dy = ciy - m[1]
    d = math.sqrt(dx**2 + dy**2)
    return d

def center(r, m, n):
    d = distanceOf2Circles(m, n)
    r1 = m[2] + r
    r2 = n[2] + r
    l = (r1**2 - r2**2 + d**2)/(2*d**2)
    e = math.sqrt((r1**2/d**2) - l**2)
    kx = m[0] + l*dx(m, n) - e*dy(m, n)
    ky = m[1] + l*dy(m, n) + e*dx(m, n)
    return kx, ky

def distanceFromStart(x):
    l = math.sqrt(x[0]**2 + x[1]**2)
    return l

def distanceFromLine(u, v, mx, my): #
    l2 = (u[0]-v[0])**2 + (u[1]-v[1])**2
    if l2 == 0:
        d = math.sqrt((u[0]-mx)**2 + (u[1]-my)**2)
    else:
        t = ((mx-u[0])*(v[0]-u[0]) + (my-u[1])*(v[1]-u[1]))/l2
        if t > 1:
            t = 1
        if t < 0:
            t = 0
        px = u[0] + t*(v[0] - u[0])
        py = u[1] + t*(v[1] - u[1])
        d = math.sqrt((px - mx)**2 + (py - my)**2) 
    return d


import argparse, math, sys, random, copy
parser = argparse.ArgumentParser()
parser.add_argument("-items", "--items", type=int, help="how many items you want to be added")
parser.add_argument("-r", "--radius", type=int, help="the standard radius")
parser.add_argument("--min_radius", type=int, help="minimum radius of the circles")
parser.add_argument("--max_radius", type=int, help="maximum radius of the circles")
parser.add_argument("-b", "--boundary_file", help="a file containing the boundaries of the area")
parser.add_argument("-s", "--seed", type=float)
parser.add_argument("output_file", help="name of output file")
args = parser.parse_args()
if args.items:
    items = args.items
else:
    items = sys.maxsize

if args.radius:
    r = args.radius
else:
    random.seed(args.seed)
    r = random.randint(args.min_radius, args.max_radius)
f = open(args.output_file, "w")
coord = []
if args.boundary_file:
    with open(args.boundary_file) as b:
        for line in b:
            x1, y1, x2, y2 = [float(x) for x in line.split()]
            coord.append((x1, y1))
            coord.append((x2, y2))
            f.write(str(x1))
            f.write(" ") 
            f.write(str(y1))
            f.write(" ")  
            f.write(str(x2))
            f.write(" ")  
            f.write(str(y2))
            f.write("\n")

metwpo = {}
circles = {}
i = 1
circles[i] = [0, 0, r]
if not(args.radius):
    r = random.randint(args.min_radius, args.max_radius)
i += 1
circles[i] = [r + circles[i-1][2], 0, r]
metwpo[i-1] = [i, i]
metwpo[i] = [i-1, i-1]
alive = [i-1, i]

while i < items and len(alive) > 0:
    min = sys.maxsize
    if (args.boundary_file):
        for a in alive: #loop gia thn euresh kuklou kontinoterou sthn arxh
            d = round(distanceFromStart(circles[a]), 2)
            if d < min:
                min = d
                kontinoteros = a
            if d == min:
                if a < kontinoteros:
                    kontinoteros = a
    else:
        for a in metwpo: #loop gia thn euresh kuklou kontinoterou sthn arxh
            d = round(distanceFromStart(circles[a]), 2)
            if d < min:
                min = d
                kontinoteros = a
            if d == min:
                if a < kontinoteros:
                    kontinoteros = a

    flag = False # thelw na ginetai oso xtupaw panw se kyklo
    if not(args.radius):
            r = random.randint(args.min_radius, args.max_radius)
    if args.boundary_file:
        copymetwpo = copy.deepcopy(metwpo)
        dead = []
        kontinoteroi = []
    while flag != True: #λοοπ για ευρεση cj
        cn = metwpo[kontinoteros][1]
        x , y = center(r, circles[kontinoteros], circles[cn])
        x , y = round(x, 2), round(y, 2)
        epomenoscn = metwpo[cn][1]
        prohgcn = metwpo[cn][0]
        flag1, flag2 = True, True # 2 boolean gia na vrw pote sunanthsa kuklo pou temnetai
        w = 0

        if len(metwpo)%2 == 1: #den
            stop = (len(metwpo)-1)/2
        else:
            stop = len(metwpo)/2
        while flag1 and flag2:
            w += 1
            if w > stop:
                break
            di = distanceof2Circles(circles[epomenoscn], x, y)
            di2 = distanceof2Circles(circles[prohgcn], x, y)
            if round(di,2) < (r + circles[epomenoscn][2]):
                cj = epomenoscn
                flag1 = False
                break
            elif round(di2, 2) < (r + circles[prohgcn][2]) and prohgcn != kontinoteros:
                cj = prohgcn
                flag2 = False
                break
            epomenoscn = metwpo[epomenoscn][1]
            prohgcn = metwpo[prohgcn][0]

        if flag1==False: #tote vrhka temnomeno kuklo phgainontas pros ton cm ara autos tha epetai tou cn 
            x = metwpo[kontinoteros][1] # o epomenos tou cm
            x2 = metwpo[x][1] # o epomenos tou epomenou tou cm
            y = metwpo[cj][0] #o 
            afairw = True
            while afairw:
                if y==x:
                    afairw = False
                del metwpo[x]
                if args.boundary_file:
                    if x in alive:
                        alive.remove(x)
                        dead.append(x)
                        kontinoteroi.append(kontinoteros)
                x = x2
                x2 = metwpo[x2][1]
            metwpo[kontinoteros][1] = cj
            metwpo[cj][0] = kontinoteros
        elif flag2==False: # tote vrhka temnomeno phgainontas pros ton cn pros ta pisw ara tha prohgeitai tou cm
            
            x = metwpo[cj][1] # o epomenos tou cj
            x2 = metwpo[x][1] # o epomenos tou epomenou tou cj poy tha xreiastei na diagraftei an x!=y
            y = metwpo[cn][0] # o prohgoumenos tou cn mexri ton opoio prepei na diagrapsw
            afairw = True
            while afairw:
                if y == x:
                    afairw = False
                del metwpo[x]
                if args.boundary_file:
                    if x in alive:
                        alive.remove(x)
                        dead.append(x)
                        kontinoteroi.append(kontinoteros)
                x = x2
                x2 = metwpo[x2][1] 
            kontinoteros = cj
            metwpo[kontinoteros][1] = cn
            metwpo[cn][0] = kontinoteros
            
        else:
            flag3 = True
            if args.boundary_file:
                for a in range(-1, len(coord)-2):
                    if distanceFromLine(coord[a+1], coord[a+2], x, y) < r:
                        flag3 = False
                        break
            if flag3:
                i += 1
                circles[i] = [x, y, r]
                metwpo[i] = [kontinoteros, cn]
                metwpo[kontinoteros][1] = i
                metwpo[cn][0] = i      

                flag = True # evala ton kuklo poy hthela ara proxwraw na vrw allon kontinotero, cn kai upopshfio kuklo
                if args.boundary_file:
                    for i in metwpo.keys():
                        if i not in alive:
                            alive.append(i)
            else:
                metwpo = copymetwpo
                for b in dead:
                    if (b not in alive) and (b not in kontinoteroi):
                        alive.append(b)
                if kontinoteros in alive:
                    alive.remove(kontinoteros)
                flag = True
print(i)
for a in circles:
    for i in circles[a]:
        f.write(str(i))
        f.write(" ") 
    f.write("\n")


