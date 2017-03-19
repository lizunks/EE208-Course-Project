import cv2
import numpy as np
import time
def feature(img):
    p = []
    h = img.shape[0]
    w = img.shape[1]
    for i in range(16):
        s = 0
        blue = 0
        green = 0
        red = 0
        for j in range((i/4)*(h/4),(i/4)*(h/4)+h/4):
            for k in range((i%4)*(w/4), (i%4)*(w/4)+w/4):
                blue+=img[j,k,0]
                green+=img[j,k,1]
                red+=img[j,k,2]
        s = blue + green + red
        if s!=0:
            p.append(float(blue)/s)
            p.append(float(green)/s)
            p.append(float(red)/s)
        else:
            p.append(0)
            p.append(0)
            p.append(0)
    for i in range(len(p)):
        if p[i] < 0.3:
            p[i] = 0
        else:
            if p[i] < 0.6:
                p[i] = 1
            else:
                p[i] = 2
    
    return p

def Hash(p):
    vp = []
    gp = ""
    for cp in p:
        for i in range(cp):
            vp.append(1)
        for i in range(2-cp):
            vp.append(0)
##    for i in range(len(proj)):
##        gp += str(vp[proj[i]])
    for i in range(len(vp)):
        gp += str(vp[i])
    return gp

def hashtable(collections):
    table = {}
    for i in range(len(collections)):
        p = feature(collections[i][0])
        gp = Hash(p,proj)
        if table.has_key(gp):
            table[gp].append(collections[i])
        else:
            table[gp] = [collections[i]]
    return table

def surf_match(target, candidates, N):
    surf = cv2.SURF()
    origin_inf = surf.detectAndCompute(target,None)
    matcher = cv2.BFMatcher() 
    num_points = 0
    best_img = second_best = None
    pic = {}
    for (img,info) in candidates:
#        print img
        if cv2.imread('pic\\'+img) == None: continue
        img_inf = surf.detectAndCompute(cv2.imread('pic\\'+img),None)
        matched = matcher.knnMatch(img_inf[1],origin_inf[1],k = 2)
        good = []
        for m,n in matched:
            if m.distance < 0.1*n.distance:
                good.append(m)
        if pic.has_key(len(good)):
            pic[len(good)].append((img,info))
        else:
            pic[len(good)] = [(img,info)]
    pic = sorted(pic.iteritems(),key=lambda asd:asd[0],reverse = True)
    result = []
    i = 0
    while len(result) < N:
        result+=pic[i][1]
        i += 1
    return result[:N+1]

def search(target, table):
    p = feature(target)
    gp = Hash(p,proj)
    candidates = []
    distances = []
    for hamming in table.keys():
        distance = 0
        for i in range(len(hamming)):
            if hamming[i] != gp[i]:
                distance += 1
        distances.append(distance)
    min_ = min(distances)
    for i in range(len(distances)):
        if(distances[i]==min_):
            candidates+=table[table.keys()[i]]
    if len(candidates)==1:
        l = distances[:]
        l.sort()
        second = l[1]
        for i in range(len(distances)):
            if distances[i] == second:
                candidates.append(table.keys()[i])
    result = surf_match(target,candidates)
    return result

def Search(name):
    start = time.clock()
    N = 20
##    proj = [1,2,3,5,7,11,13,17,19,23,29,31]

##    collections = []
##    img_list = open('LIST.TXT','r')
##    for i in img_list:
##        pic_name = ''.join(i.split())
##        img = cv2.imread(pic_name)
##        if img==None: continue
##        info = [img,pic_name]
##        collections.append(info)
##    table = hashtable(collections,proj).items()
##    img_list.close()
##    hash_list = open('table.txt','w')
##    for i in range(len(table)):
##        data = open(table[i][0]+'.txt','w')
##        hash_list.write(table[i][0]+'\n')
##        for j in range(len(table[i][1])):
##            data.write(table[i][1][j][1]+'\n')
##        data.close()
##    hash_list.close()


    target = cv2.imread(name)
    index = open('new\\LIST.TXT','r')
    codes = []
    for i in index:
        codes.append(''.join(i.split()))
    index.close()
    p = feature(target)
    gp = Hash(p)
    distances = {}
    for code in codes:
        dis = 0
        for i in range(len(code)):
            if code[i]!= gp[i]: dis+=1
        if distances.has_key(dis):
            distances[dis].append(code)
        else:
            distances[dis] = [code]
    distances = sorted(distances.iteritems(),key=lambda asd:asd[0])
    item = 0
    candidates = []
    while item >= 0:
        for i in range(len(distances[item][1])):
            data = open('new\\'+distances[item][1][i]+'.txt')
            for line in data:
                n = line.split()
                if(len(n) <= 5):continue
                candidates.append((n[1],line))
##                print name
                if (len(candidates)>2*N): break
            data.close()
        if len(candidates) > N:
            break
        else:
            item = item + 1
##    print len(candidates)
    result = surf_match(target,candidates, N) #result
##    print time.clock()-start
    url = []
    imgurl = []
    description = []
    name = []
    rate = []
    for (img,info) in result:
        n = info.split()
        url.append(n[0])
        name.append(n[1])
        imgurl.append(n[2])      
        rate.append('')
        description.append(n[4].decode('gbk'))
##    for i in range(len(result)):
##        if i > 6: break
##        cv2.imshow('result'+str(i),cv2.imread('pic\\'+result[i]))    
    return url,imgurl,description,rate


##    for i in range(1,N+1):
##        cv2.imshow('result'+str(i),cv2.imread(candidates[i]))    


##    for line in hash_list:
##        info = line.split()
##        table[info[0]]=[]
##        for i in range(1,len(info)):
##            table[info[0]].append(cv2.imread(info[i]))
##    result= search(target,table, proj)
##    cv2.imshow('target',target)
##    for i in range(1,len(result)):
##        cv2.imshow('result'+str(i),result[i])
##    hash_list.close()
