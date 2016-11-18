import math

class id3:
	def __init__(self, dataset):
		# our training dataset
		self.train = dataset.train_dataset
		# our testing dataset
		self.test = dataset.test_dataset
		# our pruning dataset
		self.prune = dataset.prune_dataset
		# for ease of debugginh lets assign feature names to each feature.
		attributes = []
		for i in range(len(self.train[0])):
			attributes.append("attr%d" % i)
		# create decision tree
		# train over train dataset
		tree = DecisionTree(self.train, attributes, attributes[-1])
		
		# test algorithm over the testing dataset
		results = []
		for row in self.test:
			# make a copy of the dicision tree
			temp_tree = tree.tree.copy()
			result = ""
			# search/predict category for this test row
			while(isinstance(temp_tree, dict)):
				root = Node(list(temp_tree.keys())[0], temp_tree[list(temp_tree.keys())[0]])
				temp_tree = temp_tree[list(temp_tree.keys())[0]]
				index = attributes.index(root.value)
				value = row[index]
				if(value in temp_tree.keys()):
					child = Node(value, temp_tree[value])
					result = temp_tree[value]
					temp_tree = temp_tree[value]
				else:
					result = "Null"
					break
			# check if the predicted category is correct?
			# if yes, insert true in results or false
			if result != "Null":
				results.append(result == row[-1])
		
		# calculate and print accuracy
		print("ID3 Accuracy %f" % (float(results.count(True))/float(len(results))))

# node class for nodes in the tree
class Node():
	def __init__(self, value, dictionary):
		self.value = value
		if (isinstance(dictionary, dict)):
			self.children = dictionary.keys()
		else:
			self.children = []

class DecisionTree():
	def __init__(self, train, attributes, target):
		self.tree = self.build_tree(train, attributes, target)
	
	'''
	this function will scan through the training dataset
	and will build the dicision tree 
	'''
	def build_tree(self, dataset, attributes, target):
		values = [record[attributes.index(target)] for record in dataset]
		default = self.majorClass(attributes, dataset, target)

		if not dataset or (len(attributes) - 1) <= 0:
			return default
		elif values.count(values[0]) == len(values):
			return values[0]
		else:
			best = self.attr_choose(dataset, attributes, target)
			tree = {best:{}}
		
			for val in self.get_values(dataset, attributes, best):
				new_data = self.get_data(dataset, attributes, best, val)
				newAttr = attributes[:]
				newAttr.remove(best)
				subtree = self.build_tree(new_data, newAttr, target)
				tree[best][val] = subtree
		return tree
	
	'''
	this function will find a root feature for the tree
	'''
	def majorClass(self, attributes, dataset, target):
		frequency = {}
		target_index = attributes.index(target)
		_max = 0
		major = ""
		
		for row in dataset:
			if row[target_index] in frequency.keys():
				frequency[row[target_index]] += 1 
			else:
				frequency[row[target_index]] = 1
		for key in frequency.keys():
			if frequency[key]>_max:
				_max = frequency[key]
				major = key
		return major
	
	def entropy(self, attributes, data, target):
		frequency = {}
		data_entropy = 0.0
		i = 0
		for row in attributes:
			if (target == row):
				break
			i = i + 1
		i = i - 1
		for row in data:
			if (row[i] in frequency):
				frequency[row[i]] += 1.0
			else:
				frequency[row[i]]  = 1.0
		for frequency in frequency.values():
			data_entropy += (-frequency/len(data)) * math.log(frequency/len(data), 2) 
		return data_entropy

	def info_gain(self, attributes, data, attr, target):
		frequency = {}
		subset_entropy = 0.0
		i = attributes.index(attr)
		for row in data:
			if (row[i] in frequency):
				frequency[row[i]] += 1.0
			else:
				frequency[row[i]]  = 1.0
		for value in frequency.keys():
			value_prob = frequency[value] / sum(frequency.values())
			dataSubset = [row for row in data if row[i] == value]
			subset_entropy += value_prob * self.entropy(attributes, dataSubset, target)
		return self.entropy(attributes, data, target) - subset_entropy

	'''
	this function chooses the best attribute maximizing the infomation gain
	'''
	def attr_choose(self, data, attributes, target):
		best = attributes[0]
		maxGain = 0;
		for attribute in attributes:
			newGain = self.info_gain(attributes, data, attribute, target) 
			if newGain > maxGain:
				maxGain = newGain
				best = attribute
		return best

	def get_values(self, data, attributes, attr):
		index = attributes.index(attr)
		values = []
		for row in data:
			if row[index] not in values:
				values.append(row[index])
		return values

	def get_data(self, data, attributes, best, val):
		new_data = [[]]
		index = attributes.index(best)
		for row in data:
			if (row[index] == val):
				newEntry = []
				for i in range(0,len(row)):
					if(i != index):
						newEntry.append(row[i])
				new_data.append(newEntry)
		new_data.remove([])    
		return new_data