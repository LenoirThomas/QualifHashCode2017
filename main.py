from Instance import Instance
from Solution import Solution



def example():
	##example in the pdf
	i = Instance()
	i.read_file("streaming/test.txt")
	s = Solution(i)
	# s.s = [
	# 	{3 : [1], 4:[],1:[1,2] },# endpoint 0, the video 3 is in the cache1 , the video 4 in none , the video 1, in the cache 0 and 2 
	# 	{0 : []}
	# ]
	s.glouton()
	print s.get_score()



if __name__ == "__main__":

	# i = Instance()
	# i.read_file("streaming/me_at_the_zoo.in")
	# i.print_i()
	example()