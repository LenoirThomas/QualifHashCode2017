import random as rand

class Solution(object):

	def __init__(self, inst):
		self.inst = inst


		# endpoint => video => cache
		# dim 1 => list of dico by endpoint
		# dim 2 => key = video, value = list of id cache servers
		self.s = [ {} for i in range(self.inst.E) ]
		#the endpoint r[1] request the video r[0], doesn't have any cache server yet...
		for r in self.inst.requests	:
			self.s[r[1]][r[0]] = []

		# the quantity of mo by cache server, must be less than inst.X
		self.caches = [[0,[]] for _ in range(self.inst.C)]

	def print_s(self):
		print "="*101
		for r in range(len(self.s)):
			print "EndPoint ",r
			for k in self.s[r]:
				print "\tVideo ",k," on the cache servers : ",self.s[r][k]
		print "="*100
	def print_s2(self):
		print "="*101
		print "Size max = ",self.inst.X
		b = True
		for i in range(len(self.caches)):
			print "Caches ",i," : ",self.caches[i][1],"  => ",self.caches[i][0]
			if self.caches[i][0]> self.inst.X:
				b = False
		print "Affection correct : ",b
		print "="*101





	def get_score(self):
		score = 0
		nbrequest = 0
		# video rv, ask by the endpoint re, rn times
		for (rv,re,rn) in self.inst.requests:
			# min between the cacher server and data server

			# get the latency for each cache server attributed for the endpoint re containing the video rv

			latency  = [self.inst.ep[re][id_cache] for id_cache in  self.s[re][rv] ]
			latency.append(self.inst.lat_data[re])# add the latency from the data server


			score += (self.inst.lat_data[re] - min(latency)) * rn
			nbrequest+= rn
		return (score*1000) / nbrequest
	def write_file(self,name):
		pass

	def glouton(self, select_func):
		## sort the request by nb request / size => the more there are requests 
		request = sorted(self.inst.requests, key = lambda x: x[2]/self.inst.vs[x[0]], reverse= True)
		for r in request:
			# get the cache servers which are connected to the endpoint r[1]
			cache_servers = self.inst.ep[r[1]]# its a dict
			video_size = self.inst.vs[r[0]]
			#print "cache_servers for the endpoint ",r[1]," : ",cache_servers
			indexs = []
			for id_cache in cache_servers:
				#print self.caches[id_cache]+video_size," ",self.inst.X
				if self.caches[id_cache][0]+video_size < self.inst.X and r[0] not in self.caches[id_cache][1]: # take only the servers which can be 
					## appedn a triplet = (id cache, nb megab on this cache, the latency ) 
					indexs.append((id_cache,self.caches[id_cache][0], cache_servers[id_cache]))

			if indexs:
				## ......... select a cache server among these
				
				index = select_func(indexs)
				self.s[r[1]][r[0]].append(index[0])
				self.caches[index[0]][0] += video_size
				self.caches[index[0]][1].append(r[0])
				## ..........

	# indexs => list of triplet (id cache, nb mega bits on this cache, latency)
	def select_random(self, indexs):
		return indexs[rand.randint(0,len(indexs)-1)]

	def select_low_latency(self,indexs):
		return min(indexs , key = lambda x:x[2])

	def select_low_cache(self,indexs):
		return min(indexs , key = lambda x:x[1])

	def select_wtf(self,indexs):
		return min(indexs , key = lambda x:x[1]*x[2])

	
	













