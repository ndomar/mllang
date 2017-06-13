#!/usr/bin/env python
"""
This is a module that contains parsing methods for the XML files.
"""
import xml.etree.ElementTree as ET
from lxml import etree
import traceback
import itertools as it

class Parser(object):

	def __init__(self):
		self.parsed = False
		self.schema =  'schema.xsd'
		self.predictors = []
		self.predictors_types = []
		self.preprocessing_methods = []


	def parse_file(self, file_path):
		"""
		Method parses an xml file given a path. It sets instance variables
		to be accessible via getters.

		:param str file_path
		"""
		root = ET.parse(file_path).getroot()
		## parse predictors
		predictors = root.find('DataSpecification').find('Predictors')
		for predictor in predictors.findall('predictor'):
			self.predictors.append(predictor.find('name').text)
			self.predictors_types.append(predictor.find('VariableType').text)
		## parse method
		method = root.find('Method')
		variables = {}
		for variable in method[0]:
			tag = variable.tag
			values = []
			for v in variable:
				values.append(float(v.text))
			variables[tag] = values
		self.variables = variables
		self.method_name = method[0].tag
		## parse pre-processing
		preprocessing = root.find('Preprocessing')
		preprocessing_methods = preprocessing.findall('PreprocessMethod')
		for preprocessing_method in preprocessing_methods:
			self.preprocessing_methods.append(preprocessing_method.text)
		evaluation = root.find('Evaluation')
		resampling = evaluation.find('Resampling')
		cv = resampling.find('CrossValidation')
		self.k = cv[0].text
		self.metric = evaluation.find('Metric').text
		self.data_split = evaluation.find("DataSplit").find('partitionRate').text
		## parse resampling
		self.plotting_file_name = root.find('Plotting').find('Plot').find('filename').text

	def get_splits(self):
		return self.k

	def get_plotting_file_name(self):
		return self.plotting_file_name

	def get_evaluation_metric(self):
		return self.metric

	def get_partition_rate(self):
		return self.data_split

	def get_preprocessing_methods(self):
		return self.preprocessing_methods

	def get_method_name(self):
		return self.method_name

	def get_predictors_types(self):
		return self.predictors_types

	def get_predictors(self):
		return self.predictors

	def get_variables(self):
		return self.variables
	
	def get_all_combinations(self, hash_set):
		"""
		The method retuns all possible combinations of the hyperparameters.

		:returns: array of dicts containing all combinations
		:rtype: list[dict]

		>>> get_all_combinations({'_lambda': [0, 0.1], 'n_factors': [20, 40]})
		[{'n_factors': 20, '_lambda': 0}, {'n_factors': 40, '_lambda': 0},
		{'n_factors': 20, '_lambda': 0.1}, {'n_factors': 40, '_lambda': 0.1}]
		"""
		names = sorted(hash_set)
		return [dict(zip(names, prod)) for prod in it.product(
		*(hash_set[name] for name in names))]

	def validate(self, xmlfilename, xsdfilename):
		data = open(xsdfilename, 'rb') 
		schema_root = etree.XML(data.read())
		schema = etree.XMLSchema(schema_root)
		xmlparser = etree.XMLParser(schema=schema)
		try:
			with open(xmlfilename, 'rb') as f:
				etree.fromstring(f.read(), xmlparser)
			print("XML file was parsed without errors")
			return True
		except etree.XMLSchemaError:
			print("Error parsing XML file")
			traceback.print_tb()
			return False

	def _to_str(self):
		print("predictors: {}, types: {} \n method: {}, preprocessing: {}\
			  \n partition_rate: {}, metric: {}, file name: {}".format(
			  self.predictors, self.predictors_types, self.method_name,
			  self.preprocessing_methods, self.data_split, self.metric,
			  self.plotting_file_name))
