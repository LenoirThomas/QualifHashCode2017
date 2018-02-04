
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
            print "Caches ", i, " : ", self.caches[i][1], "  => ", self.caches[i][0]
            if self.caches[i][0] > self.inst.X:
                b = False
        print "Affection correct : ", b
        print "=" * 101

    # return the videos requested by the endpoints conncted with the cache server id_cs
    def get_videos_by_cs(self, id_cs):
        videos_by_cs = defaultdict(int)
        for (id_ep, _) in self.inst.ep_by_caches[id_cs]:
            for (id_v, nb_request) in self.inst.videos_by_ep[id_ep].items():
                videos_by_cs[id_v] += nb_request
        return videos_by_cs

    def knapsack(self):
        # res = []
        for i in range(self.inst.C):
            #print i, "/", self.inst.C
            # res.append([])
            videos_by_cs = self.get_videos_by_cs(i)
            videos_sorted = sorted(videos_by_cs.items(),
                                   key=operator.itemgetter(1), reverse=True)
            sum_size = 0
            k = 0
            while sum_size <= self.inst.X and k < len(videos_sorted):
                id_v = videos_sorted[k][0]
                # res[i].append(id_v)
                if sum_size + self.inst.vs[id_v] <= self.inst.X:
                    self.caches[i].append(id_v)
                    sum_size += self.inst.vs[id_v]
                k += 1

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

    def glouton(self,select_func):
        # sort the request by nb request / size => the more there are requests 
        request = sorted(self.inst.requests.items(), key = lambda x: x[1]/self.inst.vs[x[0][0]], reverse= True)
        for ((id_v,id_e),nbr) in request:
            
            # get the cache servers which are connected to the endpoint r[1]
            cache_servers = self.inst.ep[id_e]# its a dict
            video_size = self.inst.vs[id_v]
            # print "cache_servers for the endpoint ",r[1]," : ",cache_servers
            indexs = []
            sum_size=0
            for id_cache in cache_servers:
                # print self.caches[id_cache]+video_size," ",self.inst.X
                if sum_size+video_size <= self.inst.X and id_v not in self.caches[id_cache]: # take only the servers which can be 
                    # appedn a triplet = (id cache, nb megab on this cache, the latency ) 
                    indexs.append((id_cache,sum_size, cache_servers[id_cache]))
            if indexs:
                # ......... select a cache server among these
                index = select_func(indexs)
                sum_size+=video_size
                self.caches[index[0]].append(id_v)
        return 0

    # def glouton2(self):














