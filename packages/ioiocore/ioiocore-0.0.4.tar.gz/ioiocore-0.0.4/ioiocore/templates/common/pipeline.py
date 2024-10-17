from ...pattern.io_pipeline import IOPipeline
from .node import Node

class Pipeline(IOPipeline):
    def __init__(self):
        IOPipeline.__init__(self)

    def add_node(self, name: str, node: Node):
        IOPipeline.add_node(self, name, node)

    def remove_node(self, name: str):
        IOPipeline.remove_node(self, name)

    def connect(self, node_name1 : str, port_name1 : str, node_name2 : str, port_name2 : str):
        IOPipeline.connect(self, node_name1, port_name1, node_name2, port_name2)

    def disconnect(self, node_name1 : str, port_name1 : str, node_name2 : str, port_name2 : str):
        IOPipeline.disconnect(self, node_name1, port_name1, node_name2, port_name2)

    def get_source_nodes(self):
        IOPipeline.get_source_nodes(self)
        
    def start(self):
        IOPipeline.start(self)

    def stop(self):
        IOPipeline.stop(self)