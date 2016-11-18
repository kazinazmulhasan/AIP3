from random import shuffle
from copy import deepcopy
from k_nearest_neighbor import *
# from naive_bayes import *
# from tan import *
from id3 import *

class Load_dataset:
	def __init__(self, file_path):
		self.file_path = file_path
		# initialize the datasets with empty list/dict
		self.original_dataset = {}
		self.train_dataset = []
		self.test_dataset = []
		self.prune_dataset = []
		# print("loading dataset: %s" % file_path)
		# read the dataset file
		self.readfile()
		# shuffle all the rows inside the dataset
		self.shuffle_dataset()
		# split the datasets into train, test and prune datasets
		self.split_dataset()
		# no longer need the original dataset
		# so lets delete it to save space
		self.original_dataset = {}
		# print("dataset has been loaded")
		# print("Train Dataset: %d rows" % len(self.train_dataset))
		# print("Test Dataset: %d rows" % len(self.test_dataset))
		# print("Prune Dataset: %d rows" % len(self.prune_dataset))
		# print()

	def readfile(self):
		flink = open(self.file_path, "r")
		# read a line from the file
		row = flink.readline()
		# if we read anything from the file, do...
		while row:
			# convert the string data to list
			row = row.split(",")
			# add the new row in correct dataset
			self.addrow(row)
			# read next line
			row = flink.readline()
		flink.close()

	def addrow(self,row):
		# retrive the class from the row
		category = row[-1]
		# put row in orignal dataset
		# insert by category
		if category not in self.original_dataset:
			# new category found
			# create a list with this new category
			self.original_dataset[category] = []
		# insert the row inside its category
		self.original_dataset[category].append(row)
	
	def shuffle_dataset(self):
		for category in self.original_dataset:
			# using shuffle func from random library
			shuffle(self.original_dataset[category])
	
	def split_dataset(self):
		# split and append in train, test and prune dataset
		# for each category
		for category in self.original_dataset:
			# count how many rows we have for current category
			rows_count = len(self.original_dataset[category])
			if rows_count >= 25: # 10:10:5 ratio
				# extend our datasets
				self.train_dataset.extend(self.original_dataset[category][:rows_count//5*2])
				self.test_dataset.extend(self.original_dataset[category][rows_count//5*2:rows_count//5*4])
				self.prune_dataset.extend(self.original_dataset[category][rows_count//5*4:])
			else: # 1:1:1 ratio
				# extend our datasets
				self.train_dataset.extend(self.original_dataset[category][:rows_count//3])
				self.test_dataset.extend(self.original_dataset[category][rows_count//3:rows_count//3*2])
				self.prune_dataset.extend(self.original_dataset[category][rows_count//3*2:])

def Run_over_dataset(file_path):
	# run each algorithm 5 times with same datasets
	for i in range(5):
		dataset1 = Load_dataset(file_path)
		# switch train and test
		dataset2 = deepcopy(dataset1)
		dataset2.train_dataset = dataset1.test_dataset
		dataset2.test_dataset = dataset1.train_dataset
		k_nearest_neighbor(dataset1)
		k_nearest_neighbor(dataset2)
		# naive_bayes(dataset1)
		# naive_bayes(dataset2)
		# tan(dataset1)
		# tan(dataset2)
		id3(dataset1)
		id3(dataset2)
		print()

if __name__ == "__main__":
	# Run_over_dataset("datasets/breast-cancer-wisconsin.data.txt")
	# Run_over_dataset("datasets/glass1.data.txt")
	# Run_over_dataset("datasets/glass2.data.txt")
	Run_over_dataset("datasets/house-votes-84.data.txt")
	# Run_over_dataset("datasets/iris.data.txt")
	# Run_over_dataset("datasets/soybean-small.data.txt")