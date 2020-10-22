#python3

#AUTHOR: Vansh Jain
#HANDLE: VanshJain-me

#TickerCompilation.py
#Comfiles the tickers from various files.

import pandas as pd
import os

class TickerCompiler:
	"""
	This class will take in data from the unstructured
	ticker files and compiles them into tickers.csv
	"""

	
	def __init__(self, file, drop_columns, 
		column_name_change):
		"""
		Defines class' variables
		"""

		self.file = file
		self.drop_columns = drop_columns
		self.column_name_change = column_name_change
		self.data_destination = "tickers.csv"


	def data_ingestion(self):
		"""
		Takes in data from unstructred files formats and
		inputs the data in a structured manner. 
		"""

		data = pd.read_csv(self.file)
		return(data)

	
	def meaningless_column_removal(self, data):
		"""
		Removes meaninless data columns 
		"""

		for column in self.drop_columns:
			if column in data.columns:
				del data[column]

		return(data)


	def column_rename(self, data):
		"""
		Renames the columns for uniform formatting and 
		aesthetic purposes
		"""

		for name in self.column_name_change:
			if name in data.columns:
				data = data.rename(columns = 
					{name: self.column_name_change[name]})
				#print("COLUMN CHANGED!")
				#print(data.head())

		return(data)


	def column_format(self, data):
		"""
		Format's the columns before adding to tickers.csv
		"""

		data = self.meaningless_column_removal(data)
		data = self.column_rename(data)
		return(data)


	def data_input(self, data):
		"""
		Inputs the tickers' data into the file
		"""

		tickers_filename = "tickers.csv"

		with open(tickers_filename, 'a') as file:
			data.to_csv(file, header=file.tell()==0, 
				index = False)


	def duplicate_removal(self):
		"""
		Removes all duplicate rows and columns in the 
		dataframe
		"""

		data = pd.read_csv("tickers.csv")
		os.remove("tickers.csv")

		isDuplicate = data.duplicated(subset=['Ticker'],
			keep='first')
		data['isDuplicate'] = isDuplicate
		data = data[data.isDuplicate != True]
		del data['isDuplicate']

		self.data_input(data)


	def compile(self):
		"""
		Takes in unstructured data, formats and stores it
		in a structured format
		"""

		tickers_data = self.data_ingestion()
		tickers_data = self.column_format(tickers_data)
		self.data_input(tickers_data)
		self.duplicate_removal()


if __name__ == "__main__":
	
	files = ["ticker_list.csv","XASE_tickers.csv",
	"XNYS_tickers.csv"]
	drop_columns = ["Quandl_Code"]
	names = {
		"ticker" : "Ticker",
		"issuer_name": "Security Name"
	}

	for file in files:
		compiler = TickerCompiler(file, drop_columns, names)
		compiler.compile()