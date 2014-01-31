import csv
import time

path = list()
summ = list()
summ.append(0)
link_path = list()
sure_path = list()
sure_path.append([0,0])

#
# My three algorithms: Nearest neighbor, repeated nearest neighbor, cheapest link
# go_cheap() implements the nearest neighbor algorithm. This is working properly.
# The main function does repeated applications of go_cheap to obtain the repeated neareste neighbor funtion.
# The different results are because where you start for nearest neighbor matters.
# Cheapest link is not working properly. The check for three edges works, but the check for circuits
# Is not working for some reason. It seems like if the check for circuits could be made to work
# everything else would fall into place.

# My data comes from http://people.sc.fsu.edu/~jburkardt/datasets/cities/cities.html and is an adaptation of
# this file: http://people.sc.fsu.edu/~jburkardt/datasets/cities/lau15_dist.txt.

#Since the third algorithm is not workin it is difficult to compare the results of the three algorithms, but repeated
#nearest neighbor produced the best results of the working two.
#Performance-wise, nearest neighbor comes to a solution quicker (given that the other algorithm basically consists
#of repeated applications of nearest neighbor.

def main():
	with open('cities_small_rv.csv', 'rb') as csvfile:
		cityreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		rows = list()
		for row in cityreader:
			rows.append(row)

		thetime = time.time()
		print "Running Nearest Neighbor (Repeated)"
		print "-----------------------------------"
		for j in range(0,9): #This acts like a repeated nearest neighbor
			for k in range(0,len(path)):
				path.pop() #Empty path out
			summ[0] = 0 #Zero out the sum
			thetime = time.time()
			go_cheap(rows, j) #Run nearest neighbor starting at j
			thetime -= time.time()
			print thetime
			#Average Time (Nearest Neighbor): 0.000268155878240
			path.append(j) #Append the starting city
			summ[0] = summ[0] + int(rows[path[9]][path[10]]) #Add in cost for final trip to starting city
			print path
			print summ
			#From running this, I was able to determin that the cheapest paths are tied for a cost of 247
			# The are: [3, 5, 7, 9, 2, 6, 4, 8, 1, 0, 3]
			# And: [7, 9, 2, 6, 4, 8, 1, 0, 3, 5, 7]
		print "Nearest Neighbor Succesful - Shortest Paths are [3, 5, 7, 9, 2, 6, 4, 8, 1, 0, 3] and [7, 9, 2, 6, 4, 8, 1, 0, 3, 5, 7]"
		#Time -0.00830006599426, -0.0134551525116, -0.0128860473633, -0.00990295410156, -0.00972986221313, -0.00972986221313, -0.0132358074188, -0.00890588760376,-0.00976920127869
		#Average (NN Repeated: -0.0088127454122


		print
		print "Running Cheapest Link"
		print "---------------------"
		cheapest_link(rows)
		print link_path
	return 0

def go_cheap(rows, current_city):
	#An implementation of nearest neighbor
	path.append(current_city) #add the current city to the path
	lowest_city = [1000, -1] #use this vecto to represent the current city
	it = 0
	for r in rows:
		rcur = int(r[current_city]) #convert to an integer from a string
		if rcur < lowest_city[0] and rcur > 0 and path.count(it) == 0:
			lowest_city[0] = rcur
			lowest_city[1] = it
		it += 1
	if len(path) < 10: #as long as the path has 9 or less nodes
		summ[0] += lowest_city[0]
		go_cheap(rows, lowest_city[1]) #recurse, next city
	return 0

def cheapest_link(rows):
	#an implementation of cheapest_link
	ix = 0
	link_future = list()
	cheapest = 1000
	for i in rows:
		jy = 0
		for j in i:
			link_future = list(link_path)
			link_future.append([ix, jy])
			#The below if statement checks if j is cheaper than the current cheapest,
			#makes sure that the xy doesn't already exist in the path, and checks whether adding
			#these xy coordinates would create a circuit or three edges.
			if int(j) < cheapest and link_path.count([ix,jy]) == 0 and is_circuit(rows, link_future) == False and three_edges(rows,link_future) == False and ix!=jy:
				cheapest = int(j)
				#link_path.append([ix, jy])
				sure_path[0] = [ix, jy]
			jy += 1
		ix += 1
	if len(link_path) < 16:
		link_path.append(sure_path[0])
		cheapest_link(rows) #recurse
	return 0

def is_circuit(rows, link_future):
	#check to see if a circuit is made, uses found path as a helper
	found = False
	for i in range(0,9):
		if found_path(rows, link_future, i):
			found = True
	return found

def found_path(row, link_future, i):
	#goes through and sees if it can get back to where it started (circuit)
	j = i
	changed = False
	is_found = False
	for m in range(0,100):
		if link_future[m%len(link_future)][0] == j:
			j = link_future[m%len(link_future)][1]
			changed = True
		if j == i and changed==True:
			is_found = True
	return is_found

def three_edges(rows,link_future):
	#checks to see if there are three edges
	xes = list()
	for i in link_future:
		xes.append(i[0])
	#print xes
	hasThree = False
	for j in range(0,9):
		if xes.count(j) < 3:
			pass
		else:
			hasThree = True
	return hasThree

if __name__ == '__main__':
	main()


