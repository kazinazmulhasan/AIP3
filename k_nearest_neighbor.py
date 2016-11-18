import operator
import re
k = 5

class k_nearest_neighbor:
	def __init__(self, dataset):
		# our training dataset
		self.train = dataset.train_dataset
		# our testing dataset
		self.test = dataset.test_dataset
		# number of times we predicted class wrong
		self.hit = 0
		# number of times we predicted class correctly
		self.miss = 0
		# if the values are categorical (not numbers)
		# we will use this table to calcuate the distance
		# between our text values
		self.distance_table = []
		
		# train and test
		self.run_test()
		# calculate accuracy of this algorithm (0 >= accuracy >= 1)
		self.cal_accuracy()
	
	def run_test(self):
		for index in range(len(self.test)):
			# get predicted category
			category = self.predic_category(self.test[index])
			# insert the predicted category end of the row
			self.test[index].append(category)
	
	def predic_category(self, testrow):
		# get neighbors for this test instance
		neighbors = self.getNeighbors(testrow)
		# vote category and return most voted category
		return self.vote_category(neighbors)
		
	
	def getNeighbors(self, testrow):
		neighbors = []
		# for each row in train, calculate distance between row
		# from the train set and the test row.
		# insert both row and the distance as neighbor
		for index in range(len(self.train)):
			neighbors.append([self.train[index], self.distance(self.train[index], testrow)])
		# sort neighbors based on distance, ascending, minimum first
		neighbors.sort(key=lambda row:row[1])
		# take first k neighbors, remove others
		neighbors = neighbors[:k]
		# extract the row and remove distance
		# return only row not distance
		for i in range(len(neighbors)):
			neighbors[i] = neighbors[i][0]
		return neighbors
	
	def distance(self, x, y):
		if re.match(r"[^0-9.-]", x[0]) is None: # quantitative data
			sum = 0
			for i in range(len(x)-1): # exclude class column
				sum += pow((float(x[i]) - float(y[i])), 2)
			return sum
		else: # categorical data
			# check if the distance table is already calculated
			# if not calculate it
			if len(self.distance_table) == 0:
				self.calculate_distance_table()
			# calculate distance
			sum = 0
			for i in range(len(x)-1): # exclude class column
				sum += pow((self.distance_table[i][x[i]] - self.distance_table[i][y[i]]), 2)
			return sum
	
	def calculate_distance_table(self):
		for i in range(len(self.train[0])):
			self.distance_table.append({})
		for row in self.train:
			for feature_index in range(len(row)):
				if row[feature_index] in self.distance_table[feature_index]:
					self.distance_table[feature_index][row[feature_index]] += 1
				else:
					self.distance_table[feature_index][row[feature_index]] = 1
		count = len(self.train)
		# print(self.distance_table)
				
	
	def vote_category(self, neighbors):
		categories = {}
		# check category of each neighbor
		for x in range(len(neighbors)):
			# get the category
			category = neighbors[x][-1]
			if category in categories:
				categories[category] += 1
			else:
				categories[category] = 1
		# sort categories based of number of votes, max first
		sortedVotes = sorted(categories.items(), key=operator.itemgetter(1), reverse=True)
		# return most voted category
		return sortedVotes[0][0]
	
	def cal_accuracy(self):
		# for each row in test dataset, check
		# if the original category and predicted
		# category is a match?
		for row in self.test:
			if row[-2:-1]==row[-1:]:
				self.hit += 1
			else:
				self.miss += 1
		# accuracy equals to number of times we predicted currect devided by
		# number of rows in test dataset
		print("Accuracy: %f" % (self.hit/len(self.test)))