
import random

class Instance(object):

    def __init__(self):

        #super(Instance, self).__init__()

        self.V = 0 ##number of videos
        self.E = 0 ## number of endpoints 
        self.U = 0 ## number of request descriptions
        self.C = 0 ## number of cache cerver
        self.X = 0##  capacity of each cache server

        # video size, list of size V
        # the id of the video corresponding to the index in the list
        self.vs = [] 
        # the latency for each endpoint from the data center
        # the id of the endpoint corresponding to the index in the list
        self.lat_data = [] 

        # the cache servers connected to each endpoint
        # an element of this list is a list containing a dico : id cache => latency
        # [ [ {id cache server1 : latency, id cache server 2 : latency}] , ...same for the endpoint 2, ...]
        self.ep = []

        # each element corresponding to a 3-uplet (id video, id endpoint , number of this requests)
        self.requests = []

    def read_file(self, name):
        f = open(name, "r")
        lines = f.readlines()
        f.close()
        # read first line
        (self.V,self.E, self.U,self.C, self.X) = (int(i) for i in lines[0].split())
        #read video sizes
        self.vs = [int(i) for i in lines[1].split()]
        # read the data enpoints
        i=2

        while len(lines[i].split())==2:
            l = lines[i].split()
            self.lat_data.append(int(l[0]))# add the latency from the data center to this endpoint
            tmp = {}
            #print l[1]
            if (int(l[1])>0):
                for k in range(1,int(l[1])+1):#browse the cache servers linked with this endpoints
                    l2 = lines[i+k].split()
                    #tmp.append((int(l2[0]), int(l2[1])))
                    tmp[int(l2[0])] = int(l2[1])
                i+=k
            i+=1
            self.ep.append(tmp)
        #print "ep = ",self.ep
            #self.ep.append( [(int(lines[i+k].split()[0],int(lines[i+k].split()[1]))) for k in range(1,int(l[1]))])
        # read the requests : 
        for k in range(i,len(lines)):
            l = lines[k].split()
            q = 0
            while q < len(self.requests) and (self.requests[q][0],self.requests[q][1])!=(int(l[0]),int(l[1])):
                q+=1
            if q == len(self.requests):
                self.requests.append([int(l[0]),int(l[1]),int(l[2])])
            else:
                self.requests[q][2]+=int(l[2])

    def print_i(self):
        print self.V," ",self.E," ",self.U," ",self.C," ",self.X
        print self.vs
        for i in range(len(self.ep)):
            print self.lat_data[i]," ",len(self.ep[i])
            for k in self.ep[i]:
                print k," ",self.ep[i][k]
        for i in range(len(self.requests)):
            print self.requests[i]

