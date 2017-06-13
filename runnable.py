from lib.task_executer import TaskExecuter
from sklearn import datasets
from lib.parser import Parser
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
iris = datasets.load_iris()
data = iris.data
labels = iris.target
if(sys.argv[1]) is None:
	print("please provide an input file")
	sys.exit(1)

xsdfilename = os.path.join(dir_path, 'xml', 'schema.xsd')
xml_input = os.path.join(dir_path, sys.argv[1])
parser = Parser()
parser.validate(xml_input, xsdfilename)
parser.parse_file(xml_input)
parser._to_str()
executer = TaskExecuter(xml_input, data, labels)

