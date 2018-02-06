
import random
from collections import defaultdict
import operator
from copy import deepcopy
import time

class Solution(object):

    def __init__(self, inst):
        self.inst = inst

        # the quantity of mo by cache server, must be less than inst.X
        self.caches = [[] for _ in range(self.inst.C)]
        self.mo_by_cs = [0 for _ in range(self.inst.C)]


    def print_s2(self):
        print "=" * 101
        print "Size max = ", self.inst.X
        b = True
        for i in range(len(self.caches)):
            print "Caches ", i, " : ", self.caches[i], "  => ", sum( [self.inst.vs[self.caches[i][j]] for j in range(len(self.caches[i]))])
            # if self.caches[i][0] > self.inst.X:
            #     b = False
        print "Affection correct : ", b
        print "=" * 101

    ######################################################################################
    # return the videos requested by the endpoints conncted with the cache server id_cs
    def get_videos_by_cs2(self, id_cs):
        videos_by_cs = defaultdict(int)
        for (id_ep, _) in self.inst.ep_by_caches[id_cs]:
            for (id_v, nb_request) in self.inst.videos_by_ep[id_ep].items():
                videos_by_cs[id_v] += ((self.inst.lat_data[id_ep]-self.inst.ep[id_ep][id_cs])*nb_request)
        return videos_by_cs

    def sort_cs(self):
        pass
    def get_dict_by_ep(self):
        l= {}
        for id_ep in range(self.inst.E):

            for (id_v, nb_reques) in self.inst.videos_by_ep[id_ep].items():
                l[(id_ep,id_v)] = False
        return l

    def aa(self):
        done = self.get_dict_by_ep()# d[ep,v] = True if the video is allocated to a cache server connected with ep
        
        mo_by_cs = [ 0 for _ in range(self.inst.C)]
        video_by_cs = [ self.get_videos_by_cs2(id_cs) for id_cs in range(self.inst.C)]

        cs = set( i for i in range(self.inst.C))

        while cs:
            best_couple=(-1,-1)
            best_score = -1
            for id_cs in cs:
                for (id_v,score) in video_by_cs[id_cs].items():
                    if score> best_score:# and mo_by_cs[i]+self.inst.vs[id_v] <= self.inst.X:
                        best_score = score
                        best_couple = (id_cs,id_v)

            # allocate the couple  cache server,video with the best score
            if mo_by_cs[best_couple[0]] + self.inst.vs[id_v] <= self.inst.X:

                self.caches[best_couple[0]].append(best_couple[1])
                mo_by_cs[best_couple[0]]+=self.inst.vs[id_v]
                # delet it to not consider it again
                del video_by_cs[best_couple[0]][best_couple[1]]
                # update the score for the other cacher servers whose the endpoints request this video....
                for (id_ep,_) in self.inst.ep_by_caches[best_couple[0]]:# all the endpoint link with this cs 
                    done[id_ep][best_couple[1]]=True
                    for (id_cs,lat) in self.inst.caches_by_ep[id_ep]:# all the cs link with this ep
                        if id_cs != best_couple[0]:
                            video_by_cs[id_cs][best_couple[0]] -= ((self.inst.lat_data[id_ep]-lat)*self.inst.videos_by_ep[id_ep][best_couple[1]])
            else:
                cs.remove(best_couple[0]) 


    ############################################################################
    ############################################################################
    def get_videos_by_cs(self, id_cs):
        videos_by_cs = defaultdict(int)
        for (id_ep, _) in self.inst.ep_by_caches[id_cs]:
            for (id_v, nb_request) in self.inst.videos_by_ep[id_ep].items():
                videos_by_cs[id_v] += ((self.inst.lat_data[id_ep]-self.inst.ep[id_ep][id_cs])*nb_request)
        return videos_by_cs

    #993 000 , en prenant just le nombre de request
    #1016360, nbrequestion / taille video
    #1020790, en utilisatnt directement le score (L - Ls)*rn
    def knapsack(self):
        # res = []
        for i in range(self.inst.C):
            #print i, "/", self.inst.C
            # res.append([])
            videos_by_cs = self.get_videos_by_cs(i)
            #videos_sorted = sorted(videos_by_cs.items(),key=operator.itemgetter(1)/self.inst.vs[operator.itemgetter(0)], reverse=True)# sort by nb request
            videos_sorted = sorted(videos_by_cs.items(),key=lambda x : x[1]/self.inst.vs[x[0]], reverse=True)# sort by nb request
            
            sum_size = 0
            k = 0
            while sum_size <= self.inst.X and k < len(videos_sorted):
                id_v = videos_sorted[k][0]
                # res[i].append(id_v)
                if sum_size + self.inst.vs[id_v] <= self.inst.X:
                    self.caches[i].append(id_v)
                    sum_size += self.inst.vs[id_v]
                k += 1
    ###########################################################################
    def get_score2(self):
        scor = 0
        nbr = 0
        for ((rv, re), rn) in self.inst.requests.items():
            latency = [self.inst.lat_data[re]]
            for (id_cs, lat) in self.inst.caches_by_ep[re]:
                if rv in self.caches[id_cs]:
                    latency.append(lat)
            scor += ((self.inst.lat_data[re] - min(latency)) * rn)
            nbr += rn
        if nbr == 0:
            return 0
        return (scor * 1000) / nbr

    # 2 022 422
    def glouton2(self):
        cs_by_v = defaultdict(int)
        #mo_by_cache = [0 for _ in range(self.inst.C)]
 
        # t0 = time.clock()
        # for id_cs in range(self.inst.C):
        #     for (id_ep, latency) in self.inst.ep_by_caches[id_cs]:
        #         for (id_v,nb_r) in self.inst.videos_by_ep[id_ep].items():
        #             cs_by_v[(id_v,id_cs)] += (nb_r * (self.inst.lat_data[id_ep] - latency))
        # print "sol 1 = ",time.clock() - t0

        #t0 = time.clock()
        ### get the score for each couple video/cache
        for ((rv,re),rn) in self.inst.requests.items():
            for (id_cs, lat) in self.inst.caches_by_ep[re]:
                cs_by_v[(rv,id_cs)]+=(rn * (self.inst.lat_data[re]- lat))
        #print "sol 2 = ",time.clock() - t0


        cs_by_v = sorted(cs_by_v.items(), key=lambda x: x[1], reverse=True)
        done = [False] * self.inst.V
        # fill the data for the score
        for ((id_v,id_cs),_) in cs_by_v:
            if not done[id_v] and self.mo_by_cs[id_cs]+self.inst.vs[id_v] <= self.inst.X:
                    self.mo_by_cs[id_cs]+=self.inst.vs[id_v]
                    self.caches[id_cs].append(id_v)
                    done[id_v] = True
        for ((id_v,id_cs),_) in cs_by_v:
            if not id_v in self.caches[id_cs] and self.mo_by_cs[id_cs]+self.inst.vs[id_v]<= self.inst.X:
                self.caches.append(id_v)
                self.mo_by_cs[id_cs]+=self.inst.vs[id_v]

    ################################

    def select_wtf(self,indexs):
        return min(indexs , key = lambda x:x[1]*x[2])




    # 1689464
    def glouton(self,select_func):
        # sort the request by nb request / size => the more there are requests 
        #done = self.get_dict_by_ep()
        request = sorted(self.inst.requests.items(), key = lambda x: x[1]/self.inst.vs[x[0][0]], reverse= True)
        
        #request = sorted(self.inst.requests.items(), key = lambda x: self.inst.lat_data[x[0][1]] - x[1]/self.inst.vs[x[0][0]], reverse= True)
        
        for ((id_v,id_e),nbr) in request:
            # get the cache servers which are connected to the endpoint r[1]
            cache_servers = self.inst.ep[id_e]# its a dict
            video_size = self.inst.vs[id_v]
            # print "cache_servers for the endpoint ",r[1]," : ",cache_servers
            indexs = []
            for id_cache in cache_servers:
                # print self.caches[id_cache]+video_size," ",self.inst.X
                if self.mo_by_cs[id_cache]+video_size <= self.inst.X and id_v not in self.caches[id_cache]: # take only the servers which can be 
                    #appedn a triplet = (id cache, nb megab on this cache, the latency ) 
                    #indexs.append((id_cache,mo_by_cs[id_cache], (self.inst.lat_data[id_e]-cache_servers[id_cache])))
                    indexs.append((id_cache,self.mo_by_cs[id_cache], cache_servers[id_cache]))
                    
            if indexs:
                # ......... select a cache server among these
                index = select_func(indexs)
                self.mo_by_cs[index[0]]+=video_size
                self.caches[index[0]].append(id_v)
                #done[(id_e,id_v)]=True

    def optimize_cache(self,id_cs):
        ###score
        score_by_video = defaultdict(int)
        eps_by_video = defaultdict(list)
        for (id_ep, lat) in self.inst.ep_by_caches[id_cs]:
            for (id_v, nb_request) in self.inst.videos_by_ep[id_ep].items():
                    score_by_video[id_v] += (nb_request * (self.inst.lat_data[id_cs] - lat))
                    eps_by_video[id_v].append(id_ep)



        ########### solve backspace by dynamic programming 

        print "==============score before = ",sum(score_by_video[i] for i in self.caches[id_cs])
        self.caches[id_cs] = []
        self.mo_by_cs[id_cs]=0

        m = [ [ 0 for _ in range(self.inst.X) ] for _ in range(len(score_by_video))]
        videos = score_by_video.items()
        # row => video 
        # column => size of the cache
        for j in range(self.inst.X):
            if self.inst.vs[videos[0][0]] <= j:
                m[0][j] = videos[0][1] 

        for i in range(1,len(score_by_video)):
            for j in range(self.inst.X):
                if j>=self.inst.vs[videos[i][0]]:
                    m[i][j] = max(m[i-1][j], m[i-1][j-self.inst.vs[videos[i][0]]]+videos[i][1])
                else:
                    m[i][j] = m[i-1][j]


        ## backtracking:
        i = len(score_by_video)-1
        j = self.inst.X -1 
        while i!=0 and j!=0:
            if m[i][j] == m[i-1][j]: # dont take the video i 
                i-=1
            else:
                self.caches[id_cs].append(videos[i][0])
                self.mo_by_cs[id_cs]+=self.inst.vs[videos[i][0]]
                j -= self.inst.vs[videos[i][0]]
                i-=1
        print "cache = ",id_cs," : ",self.caches[id_cs]," size = ",self.mo_by_cs[id_cs]
        for id_v,score in videos:
            if id_v not in self.caches[id_cs]:
                print "id_v = ",id_v," size = ",self.inst.vs[id_v]
        print "==============score after = ",sum(score_by_video[i] for i in self.caches[id_cs])


    def optimize_couple_caches(self,id_cs1,id_cs2):
        set_cs1 = set()
        set_cs2 = set()
        for (id_ep1,latency1) in self.ep_by_caches[id_cs1]:
            for (id_ep2,latency2) in self.ep_by_caches[id_cs2]:
                if id_ep1 == id_ep2:# if connected with a same endpoint
                    for v1 in self.caches[id_cs1]:
                        for v2 in self.caches[id_cs2]:
                            if v1 == v2: # 
                                pass


        print "here"

    ##########################
    def glouton3(self):
        m = [ defaultdict(int)  for i in range(self.inst.C) ]
        for k in range(self.inst.C):
            #if k == 0:#init first line
            for (id_ep,lat) in self.inst.ep_by_caches[k]:
                for (id_v,nb_r) in self.inst.videos_by_ep[id_ep].items():
                    m[k][id_v]+= nb_r
        for k in range(self.inst.C):
            s = sorted(m[k].items(),key = lambda x:x[1],reverse=True)
            mo=0
            for (id_v,nb_r) in s:
                if self.inst.vs[id_v]+mo < self.inst.X:
                    self.caches[k].append(id_v)
                    mo+= self.inst.vs[id_v]

    ## del a random key in a cache server
    def n1(self,id_cs):
        if len(self.caches[id_cs])>0:
            i = random.randint(0,len(self.caches[id_cs])-1)
            self.mo_by_cs[id_cs]-=self.inst.vs[self.caches[id_cs][i]]
            del self.caches[id_cs][i]

    def n2(self,id_cs):
        videos =self.get_videos_by_cs(id_cs)
        v = sorted(videos.items(), key = lambda x:x[1],reverse=False)
        for (id_v,score) in v:
            if self.mo_by_cs[id_cs]+self.inst.vs[id_v]<= self.inst.X:
                self.caches[id_cs].append(id_v)
                self.mo_by_cs[id_cs] +=self.inst.vs[id_v]
                break

    def recuit_simule(self):
        self.glouton(self.select_wtf)
        current = deepcopy(self)
        current_score = current.get_score2()
        print "init score = ",current_score
        for x in range(100):
            print "x = ",x
            copi =deepcopy(current)
            for id_cs in range(self.inst.C):
                for _ in range(random.randint(0,len(self.caches[id_cs]))):
                    copi.n1(id_cs)

            for id_cs in range(self.inst.C):
                copi.n2(id_cs)
            copi_score = copi.get_score2()
            if copi_score>=current_score:
                current = copi
                current_score = copi_score
                print "improve = ",copi_score


            
    # ## swap two videos 
    # def n2(self,id_cs1,id_cs2,mo_by_cs):

    #     intersection = set()
    #     for id_v1 in self.caches[id_cs1].keys():
    #         for id_v2 in self.caches[id_cs2].keys():
    #             if id_v1==id_v2:
    #                 intersection.add(id_v1)

    #     for id_v1 in intersection:
    #         for id_v2 in intersection:
    #             if id_v1 != id_v2:
    #                 if mo_by_cs[id_cs1] - self.inst.vs[id_v1] + self.inst.vs[id_v2] <= self.inst.X and
    #                     mo_by_cs[id_cs2] - self.inst.vs[id_v2] + self.inst.vs[id_v1] <= self.inst.X:
    #                     self.caches[id_cs1].appe


















