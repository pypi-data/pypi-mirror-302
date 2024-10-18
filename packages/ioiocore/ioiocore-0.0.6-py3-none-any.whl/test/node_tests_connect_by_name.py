from utilities import *
from template_nodes import *
import unittest

class NodeTests_ConnectByName(unittest.TestCase):
    def test_connect_by_name_no_disconnect(self):
        "Tests if nodes can be connected. Destructor not called actively. No error must be thrown."
        src = Source()
        filt = Filter()

        res = False
        try:
            src.connect_by_name('out1', filt, 'in1')
            res = True
        except:
            res = False
        assert res

    def test_connect_by_name_disconnect(self):
        "Tests if nodes can be connected and disconnected."
        src = Source()
        filt = Filter()

        res = False
        try:
            src.connect_by_name('out1', filt, 'in1')
            src.disconnect_by_name('out1', filt, 'in1')
            res = True
        except:
            res = False
        assert res

    def test_connect_by_name_disconnect_connect(self):
        "Tests if nodes can be connected, disconnected and connected again."
        src = Source()
        filt = Filter()

        res = False
        try:
            src.connect_by_name('out1', filt, 'in1')
            src.disconnect_by_name('out1', filt, 'in1')
            src.connect_by_name('out1', filt, 'in1')
            res = True
        except:
            res = False
        assert res

    def test_connect_by_name_duplicate_connections(self):
        "Connection attempts must fail if a node is already connected."
        src = Source()
        filt = Filter()

        res = False
        try:
            src.connect_by_name('out1', filt, 'in1')
            src.connect_by_name('out1', filt, 'in1')
            res = False
        except:
            res = True
        assert res

    def test_connect_by_name_invalid(self):
        "Invalid connection attempts must fail."
        src = Source()
        filt = Filter()

        def connect_by_name(outputPortId, node, inputPortId):
            res = False
            try:
                src.connect_by_name(outputPortId, node, inputPortId)
                res = False
            except:
                res = True
            return res

        assert connect_by_name('out1', filt, 'in10')
        assert connect_by_name('out10', filt, 'in1')
        assert connect_by_name('out1', None, 'in1')

    def test_connect_by_name_input_to_input(self):
        "It must not be possible to connect inputs to inputs."
        filt = Filter()

        res = False
        try:
            filt.connect_by_id('in1', filt, 'in1')
            res = False
        except:
            res = True
        assert res

    def test_connect_by_name_output_to_output(self):
        "It must not be possible to connect outputs to outputs."
        filt = Filter()

        res = False
        try:
            filt.connect_by_id('out1', filt, 'out1')
            res = False
        except:
            res = True
        assert res

    def test_connect_by_name_split(self):
        "It must be possible to connect multiple inputs to an output."
        filt1 = Filter()
        filt2 = Filter()

        res = False
        try:
            filt1.connect_by_name('out1', filt2, 'in1')
            filt1.connect_by_name('out1', filt2, 'in2')
            res = True
        except:
            res = False
        assert res

    def test_connect_by_name_merge(self):
        "It must not be possible to connect multiple outputs to one input."
        filt1 = Filter()
        filt2 = Filter()

        res = False
        try:
            filt1.connect_by_name('out1', filt2, 'in1')
            filt1.connect_by_name('out2', filt2, 'in1')
            res = False
        except:
            res = True
        assert res

if __name__ == '__main__':
    try:
        filePath =  os.path.join(dir, os.path.basename(__file__).replace(".py", "") + ".txt") 
        with open(filePath, "w") as f:
            dual_stream = DualStream(f, sys.stdout)
            runner = unittest.TextTestRunner(stream=dual_stream, verbosity=2)
            unittest.main(testRunner=runner, exit=False)
    except SystemExit as e:
        pass