class Impute_missing_data:
	file_path = ""
	sample_dataset = []
	missing_dataset = []

	def __init__(self, file_path):
		self.file_path = file_path

		self.readfile()
		if len(self.missing_dataset) > 0:
			self.impute_missing_data()

	def readfile(self):
		flink = open(self.file_path, "r")
		line = flink.readline()
		while line:
			self.addline(line)
			line = flink.readline()
		flink.close()

	def addline(self, data):
		pass

	def impute_missing_data(self):
		pass

if __name__ == "__main__":
	Impute_missing_data("datasets/glass.data.txt")
	# Impute_missing_data("dataset/")
	# Impute_missing_data("dataset/")