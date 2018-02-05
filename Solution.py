
import random
from collections import defaultdict
import operator


class Solution(object):

    def __init__(self, inst):
        self.inst = inst

        # the quantity of mo by cache server, must be less than inst.X
        self.caches = [[] for _ in range(self.inst.C)]

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

    def glouton2(self):
        cs_by_v = []
        mo_by_cache = [0 for _ in range(self.inst.C)]
        for id_v in range(self.inst.V):
            for id_cs in range(self.inst.C):
                eps = self.inst.ep_by_caches[id_cs]
                tmp = 0
                for (id_ep, latency) in eps:
                    if id_v in self.inst.videos_by_ep[id_ep].keys():
                        tmp += (self.inst.videos_by_ep[id_ep][id_v] * (self.inst.lat_data[id_ep] - latency))

                    cs_by_v.append((id_v, id_cs, tmp))
        cs_by_v = sorted(cs_by_v, key=lambda x: x[2], reverse=True)
        # fill the data for the score
        for (id_v,id_cs,tmp) in cs_by_v:
            # print id_v," ",id_cs," ",tmp
            video_size = self.inst.vs[id_v]
            if mo_by_cache[id_cs]+video_size <= self.inst.X:
                mo_by_cache[id_cs]+=video_size
                self.caches[id_cs].append(id_v)

    ################################

    def select_wtf(self,indexs):
        return min(indexs , key = lambda x:x[1]*x[2])




    # 1689464
    def glouton(self,select_func):
        # sort the request by nb request / size => the more there are requests 
        done = self.get_dict_by_ep()
        mo_by_cs = [0 for _ in range(self.inst.C)]
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
                if mo_by_cs[id_cache]+video_size <= self.inst.X and id_v not in self.caches[id_cache]: # take only the servers which can be 
                    #appedn a triplet = (id cache, nb megab on this cache, the latency ) 
                    #indexs.append((id_cache,mo_by_cs[id_cache], (self.inst.lat_data[id_e]-cache_servers[id_cache])))
                    indexs.append((id_cache,mo_by_cs[id_cache], cache_servers[id_cache]))
                    
            if indexs:
                # ......... select a cache server among these
                index = select_func(indexs)
                mo_by_cs[index[0]]+=video_size
                self.caches[index[0]].append(id_v)
                done[(id_e,id_v)]=True

        return done

    def optimize_cache(self,id_cs,done):
        # empty the cache server        
        self.caches[id_cs] = []
        score_by_video = defaultdict(int)
        eps_by_video = defaultdict(list)
        for (id_ep, lat) in self.inst.ep_by_caches[id_cs]:
            for (id_v, nb_request) in self.inst.videos_by_ep[id_ep].items():
                if done[(id_ep,id_v)] == False:
                #score_by_video[id_v] += ((self.inst.lat_data[id_ep]-self.inst.ep[id_ep][id_cs])*nb_request)
                    score_by_video[id_v] += nb_request
                    eps_by_video[id_v].append(id_ep)

        video_sorted = sorted(score_by_video.items(), key = lambda x:x[1], reverse = True)
        mo = 0
        for (id_v,score) in video_sorted:
            if mo + self.inst.vs[id_v] <= self.inst.X:
                self.caches[id_cs].append(id_v)
                mo += self.inst.vs[id_v]
                for id_ep in eps_by_video[id_v]:
                    done[(id_ep,id_v)]=True
        return done

    def lol(self):
        done = self.glouton(self.select_wtf)
        for id_cs in range(self.inst.C):
            done = self.optimize_cache(id_cs,done)
            print "score = ",self.get_score2()
            #self.print_s2()



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












