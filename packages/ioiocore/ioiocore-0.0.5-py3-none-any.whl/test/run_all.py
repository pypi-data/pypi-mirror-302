import unittest
import importlib
import inspect
import os
import sys
from utilities import DualStream

# folder relative to basefolder
# this folder is scanned for testcases
FOLDERS = ["test"]

def import_classes_of_type(module_name, base_class):
    module = importlib.import_module(module_name)
    return {name: cls for name, cls in inspect.getmembers(module, inspect.isclass) 
            if issubclass(cls, base_class) and cls is not base_class}

if __name__ == '__main__':
    for folder in FOLDERS:
        all_files = os.listdir(folder)
        python_files = [file for file in all_files if file.endswith(".py")]

        #execute all tests from python files
        for f in python_files:
            modulename = f.replace('.py', '')
            modulename = modulename
            classes = import_classes_of_type(modulename, unittest.TestCase)
            if len(classes) > 0:
                filePath =  os.path.join(os.path.dirname(os.path.abspath(__file__)), f.replace('.py','') + '.txt') 
                with open(filePath, "w") as f:
                    for test_case_class in classes.values():
                        dual_stream = DualStream(f, sys.stdout)
                        runner = unittest.TextTestRunner(stream=dual_stream, verbosity=2)
                        unittest.main(testRunner=runner, exit=False)

        #merge all testresults into one file
        all_files = os.listdir(folder)
        txt_files = [file for file in all_files if file.endswith(".txt")]
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_tests.txt'), 'w') as outfile:
            for filename in txt_files:
                filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),filename)
                if os.path.exists(filepath):
                    with open(filepath, 'r') as infile:
                        outfile.write(infile.read())
                        outfile.write("\n")
                else:
                    print(f"File '{filepath}' not found.")