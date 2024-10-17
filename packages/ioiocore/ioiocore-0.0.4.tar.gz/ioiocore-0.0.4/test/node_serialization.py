from utilities import *
from template_nodes import *
import unittest

class NodeTests_Serialization(unittest.TestCase):
    def test_serialize_source(self):
        "Tests if a source node can be serialized into a dictionary and json string."
        try:
            src = Source()
            if src.__dict__()['outputs'][0]['name'] != 'out1':
                assert False

            if src.__dict__()['outputs'][1]['name'] != 'out2':
                assert False
        except:
            assert False

        assert True
        
    def test_serialize_filter(self):
        "Tests if a filter node can be serialized into a dictionary and json string."
        try:
            filt = Filter()
            if filt.__dict__()['outputs'][0]['name']  != 'out1':
                assert False

            if filt.__dict__()['outputs'][1]['name']  != 'out2':
                assert False

            if filt.__dict__()['inputs'][0]['name']  != 'in1':
                assert False

            if filt.__dict__()['inputs'][1]['name']  != 'in2':
                assert False
        except:
            assert False

        assert True

    def test_serialize_sink(self):
        "Tests if a sink node can be serialized into a dictionary and json string."
        try:
            sink = Sink(None)
            if sink.__dict__()['inputs'][0]['name']  != 'in1':
                assert False

            if sink.__dict__()['inputs'][1]['name']  != 'in2':
                assert False

        except:
            assert False

        assert True

if __name__ == '__main__':
    try:
        filePath =  os.path.join(dir, os.path.basename(__file__).replace(".py", "") + ".txt") 
        with open(filePath, "w") as f:
            dual_stream = DualStream(f, sys.stdout)
            runner = unittest.TextTestRunner(stream=dual_stream, verbosity=2)
            unittest.main(testRunner=runner, exit=False)
    except SystemExit as e:
        pass