from Instance import Instance
from Solution import Solution



def example():
	##example in the pdf
	i = Instance()
	i.read_file("streaming/test.txt")
	s = Solution(i)
	s.s = [
		{3 : [1], 4:[],1:[1,2] },# endpoint 0, the video 3 is in the cache1 , the video 4 in none , the video 1, in the cache 0 and 2 
		{0 : []}
	]
	print s.get_score()
	s.glouton(s.select_low_cache)
	print s.get_score()

def glouton():
	i = Instance()
	i.read_file("streaming/me_at_the_zoo.in")
	#i.read_file("streaming/test.txt")
	#i.read_file("streaming/trending_today.in")
	#i.print_i()
	s= Solution(i)
	s.glouton(s.select_random)
	print "random select = ",s.get_score()
	#s.print_s2()
	
	s= Solution(i)
	s.glouton(s.select_low_latency)
	print "best latency select = ",s.get_score()
	#s.print_s2()

	s= Solution(i)
	s.glouton(s.select_low_cache)
	print "low cache select = ",s.get_score()
	#s.print_s2()

	s= Solution(i)
	s.glouton(s.select_wtf)
	print "wtf = ",s.get_score()
	#s.print_s2()
	s= Solution(i)
	s.glouton(s.select_wtf2)
	print "wtf2 = ",s.get_score()

	s= Solution(i)
	s.glouton2()
	print "Glouton 2  = ",s.get_score()
	s.print_s2()

	
	

if __name__ == "__main__":

	#example()
	glouton()
	
	



