from random import choice as random_sample

'''
Imputes missing data by choosing a random sample row
(from the original dataset) that is in the same
class/category as the row that needs missing data
imputation. Any row that needs missing data imputation
but original dataset doesn't contain any rows that can
be used as sample for imputation, will be remove and
will not be included in the final/imputed dataset.
System will replace the source file/original dataset
with imputed dataset with the rows in same order
they were in the original dataset.
'''

class Impute_missing_data:
	file_path = ""					# source file address
	missing_data_chr = ""			# missing data character
	sample_dataset = {}				# sample dataset that we will use to calculate probable data
	missing_dataset = {}			# dataset with all rows that have missing data
	sample_dataset_row_count = 0	# number of rows in sample dataset
	missing_dataset_row_count = 0	# number of rows in missing dataset

	def __init__(self, file_path, missing_data_chr):
		print("starting missing data imputation...")

		self.file_path = file_path
		self.missing_data_chr = missing_data_chr
		print("imputing dataset: %s" % file_path)
		print("missing data char: %s\n" % missing_data_chr)

		print("reading source file...")
		self.readfile()
		print("rows in sample dataset: %d" % self.sample_dataset_row_count)
		print("rows in missing dataset: %d\n" % self.missing_dataset_row_count)
		
		if self.missing_dataset_row_count == 0:
			print("missing dataset is empty. exiting...")
			return
		
		print("imputing missing data...")
		self.impute_missing_data()
		print("\nmerging rows to dataset...")
		self.merge_rows()
		print("saving dataset to source file...")
		self.save_dataset()
			
		print("end of missing data imputation\n")

	def readfile(self):
		flink = open(self.file_path, "r")
		# sequence number of the row in the file
		# this will help us to put the rows back
		# in same order they are in the source file
		# from this we can also conclude how many
		# rows we have read from the source file
		row_number = 0
		# read a line from the file
		row = flink.readline()
		# if we read anything from the file, do...
		while row:
			# update number of lines we read
			row_number += 1
			# convert the string data to list
			row = row.split(",")
			# insert the row number in the beginning of the list
			row.insert(0, row_number)
			# add the new row in correct dataset
			self.addrow(row)
			# read next line
			row = flink.readline()
		flink.close()
		print("rows read from file: %d\n" % row_number)

	def addrow(self,row):
		# retrive the class from the row
		category = row[-1]
		# check if there is any missing value
		miss = False # lets assume no missing value
		for feature in range(len(row)):
			if row[feature] == self.missing_data_chr:
				miss = True # one missing value found
				# one missing value is enough to conclude
				break
		# push row in the right dataset
		if miss:
			# put row in missing dataset
			if category not in self.missing_dataset:
				self.missing_dataset[category] = []
			self.missing_dataset[category].append(row)
			self.missing_dataset_row_count += 1
		else:
			# put row in sample dataset
			if category not in self.sample_dataset:
				self.sample_dataset[category] = []
			self.sample_dataset[category].append(row)
			self.sample_dataset_row_count += 1


	def impute_missing_data(self):
		# process each category/class
		for category in self.missing_dataset:
			print("imputing category: %s" % category[:-1])
			# check if we have sample data for imputation
			# if not, skip and go to next category/class
			# since, we will skip these rows, they won't
			# be included in the final dataset that will be
			# saved in the source file after imputation
			if category not in self.sample_dataset:
				print("\t~ no sample data for imputing missing data for category %d" % category)
				continue
			# retrive and impute each row until the lis is empty
			while len(self.missing_dataset[category])>0:
				# retrive a row (first row)
				row = self.missing_dataset[category].pop(0)
				# get a random row from sample dataset under same category/class
				sample = random_sample(self.sample_dataset[category])
				# check for missing value for each feature and
				# if missing, replace the value with the value
				# from randomly selected sample row
				for feature in range(1,len(row)):
					if row[feature] == self.missing_data_chr:
						row[feature] = sample[feature]
				# insert the row in sample dataset
				self.sample_dataset[category].append(row)


	def merge_rows(self):
		# create a new list to store merged dataset
		self.export = []
		# merge all rows from sample dataset
		for category in self.sample_dataset:
			while len(self.sample_dataset[category]):
				self.export.append(self.sample_dataset[category].pop())
		# since we removed the rows from missing dataset
		# during missing data imputation, no need to go
		# through the missing dataset at all.

		# since we split the dataset and join it back,
		# rows are not in the same sequence that they
		# were before, we need to sort the merged dataset
		# first column contains the row number of original sequence
		self.export.sort(key=lambda row:row[0])

	def save_dataset(self):
		# save the number of rows in the merged dataset
		row_count = len(self.export)
		# open file for writing
		flink = open(self.file_path, "w")
		# empty the file before sriting
		flink.truncate()
		# write until no row left
		while len(self.export) > 0:
			# get the first row from merged dataset
			row = self.export.pop(0)
			# remove the row number from the row
			row.pop(0)
			# write row to file
			flink.write(",".join(row))
		# close file
		flink.close()
		print("number of rows wrote to file: %d" % row_count)


if __name__ == "__main__":
	Impute_missing_data("datasets/breast-cancer-wisconsin.data.txt", "?")
	Impute_missing_data("datasets/glass.data.txt", "None")