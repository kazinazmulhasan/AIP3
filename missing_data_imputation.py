class Impute_missing_data:
	file_path = ""				# src file address
	missing_data_chr = ""		# missing data character
	col_count = 0				# number of column in the dataset
	sample_dataset = []			# sample dataset that we will use to calculate probable data
	missing_dataset = []		# dataset with all row with missing data

	def __init__(self, file_path, missing_data_chr):
		self.file_path = file_path
		self.missing_data_chr = missing_data_chr

		self.create_cols()
		self.readfile()
		print("\n%d rows in sample dataset" % len(self.sample_dataset[0]))
		print("\n%d rows in missing dataset" % len(self.missing_dataset[0]))
		if len(self.missing_dataset[0]) > 0:
			self.impute_missing_data()

	def create_cols(self):
		with open(self.file_path, "r") as flink:
			head = flink.readline()
			flink.close()
		head = head.split(",")
		self.col_count = len(head)

		print("col count: %d" % self.col_count)
		for i in range(self.col_count):
			self.sample_dataset.append([])
			self.missing_dataset.append([])


	def readfile(self):
		flink = open(self.file_path, "r")
		line = flink.readline()
		while line:
			self.addline(line)
			line = flink.readline()
		flink.close()

	def addline(self, data):
		# parse data
		data = data.split(",")
		miss = False
		for i in range(self.col_count):
			if data[i] == self.missing_data_chr:
				miss = True
		if miss:
			# put row in missing dataset
			for i in range(self.col_count):
				self.missing_dataset[i].append(data[i])
		else:
			# put row in sample dataset
			for i in range(self.col_count):
				self.sample_dataset[i].append(data[i])


	def impute_missing_data(self):
		print("imputing data")
		return

if __name__ == "__main__":
	Impute_missing_data("datasets/breast-cancer-wisconsin.data.txt", "?")
	# Impute_missing_data("dataset/")
	# Impute_missing_data("dataset/")