
from Instance import Instance
from Solution import Solution






if __name__=="__main__":
	files = ["me_at_the_zoo.in","videos_worth_spreading.in","trending_today.in","kittens.in.txt"]
	#files = ["me_at_the_zoo.in"]
	#files = ["videos_worth_spreading.in"]
	#files = ["kittens.in.txt"]		
	wtfsum=0
	knapsackscore = 0
	glouton2=0
	aascore = 0
	for file in files:
		print "=====================",file,"================="
		i = Instance()
		#i.read_file("streaming/me_at_the_zoo.in")
		#i.read_file("streaming/test.txt")
		#i.read_file("streaming/trending_today.in")
		#i.read_file("streaming/videos_worth_spreading.in")
		#i.read_file("streaming/kittens.in.txt")
		i.read_file("streaming/"+file)

		# s= Solution(i)
		# s.knapsack()
		# tmp=s.get_score2()
		# print "knapsack = ",tmp
		# knapsackscore+=tmp

		# s= Solution(i)
		# s.aa()
		# tmp=s.get_score2()
		# print "aa = ",tmp
		# aascore+=tmp

		# s= Solution(i)
		# s.recuit_simule()
		# #print s.get_score2()
		# print "="*50


		s = Solution(i)
		s.glouton2()
		tmp = s.get_score2()
		glouton2 += tmp
		print "glouton 2 =",tmp

		# s = Solution(i)
		# s.optimize_caches()
		# tmp = s.get_score2()
		# print "optimize = ",tmp

		# s = Solution(i)
		# s.glouton(s.select_wtf)
		# #s.glouton(select_low_latency)
		# tmp = s.get_score2()
		# print "glouton wtf = ",tmp
		# wtfsum+=tmp


	print "="*50
	print "score glouton 2 ",glouton2
	print "score knapsack = ",knapsackscore
	print "score wtf = ",wtfsum
	print "score aa ",aascore


	#s.glouton(s.select_random)
	#print "random select = ",s.get_score()
	

