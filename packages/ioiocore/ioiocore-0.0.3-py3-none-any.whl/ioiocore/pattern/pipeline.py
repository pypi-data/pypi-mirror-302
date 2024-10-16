from .node import Node
from .sources import *
from .constants import *

class Pipeline:
    def __init__(self):
        self.__nodes = {} 

    def add_node(self, name: str, node: Node):
        if name in self.__nodes.keys():
            raise ValueError(f"A node with the name '{name}' already exists.")
        self.__nodes[name] = node

    def remove_node(self, name: str):
        if name not in self.__nodes.keys():
            raise KeyError(f"No node found with the name '{name}'.")
        del self.__nodes[name]
    
    def __get_ports(self, n1 : Node):
        return [n1.__dict__()[NodeInfo.INPUTS.value], n1.__dict__()[NodeInfo.OUTPUTS.value]]

    def __n1_is_output(self, n1 : Node, port_name1 : str, n2 : Node, port_name2 : str ):
        n1p = self.__get_ports(n1)
        n2p = self.__get_ports(n2)
        if len(n1p[1]) == 0 and len(n2p[1]) == 0 :
            raise ValueError(f"No outputs found for {n1.__class__.__name__} or {n2.__class__.__name__}.")
        if len(n1p[0]) == 0 and len(n2p[0])== 0 :
            raise ValueError(f"No inputs found for {n1.__class__.__name__} or {n2.__class__.__name__}.")
        
        n1_isOutput = False
        if any(port_name1 in p.values() for p in n1p[0]):
            n1_isOutput = False
        if any(port_name1 in p.values() for p in n1p[1]):
            n1_isOutput = True
        if not(any(port_name1 in p.values() for p in n1p[0])) and not(any(port_name1 in p.values() for p in n1p[1])):
            raise ValueError(f'Port {port_name1} not found in {n1.__class__.__name__}.')
        if not(any(port_name2 in p.values() for p in n2p[0])) and not(any(port_name2 in p.values() for p in n2p[1])):
            raise ValueError(f'Port {port_name2} not found in {n2.__class__.__name__}.')
        return n1_isOutput

    def __check_nodes(self, node_name1 : str, node_name2 : str):
        n1 : Node = None
        try:
            n1 : Node = self.__nodes[node_name1] 
        except:
            raise ValueError(f'Pipeline does not contain \'{node_name1}\'.')
        try:
            n2 : Node = self.__nodes[node_name2]
        except:
            raise ValueError(f'Pipeline does not contain \'{node_name2}\'.')
        return [n1, n2]

    def connect(self, node_name1 : str, port_name1 : str, node_name2 : str, port_name2 : str):
        nodes = self.__check_nodes(node_name1, node_name2)
        ports = [port_name1, port_name2]
        if self.__n1_is_output(nodes[0], port_name1, nodes[1], port_name2):
            nodes[0].connect_by_name(ports[0], nodes[1], ports[1])
        else:
            nodes[1].connect_by_name(ports[1], nodes[0], ports[0])

    def disconnect(self, node_name1 : str, port_name1 : str, node_name2 : str, port_name2 : str):
        nodes = self.__check_nodes(node_name1, node_name2)
        ports = [port_name1, port_name2]
        if self.__n1_is_output(nodes[0], port_name1, nodes[1], port_name2):
            nodes[0].disconnect_by_name(ports[0], nodes[1], ports[1])
        else:
            nodes[1].disconnect_by_name(ports[1], nodes[0], ports[0])

    def get_source_nodes(self):
        sources : list[Node] = []
        for node in self.__nodes.values():
            np = self.__get_ports(node)
            if len(np[0]) == 0 and len(np[1]) > 0:
                sources.append(node)    
        if len(sources) is None:
            raise ValueError(f'No source node was found.')
        return sources
        
    def start(self):
        found = False
        for node in self.__nodes.values():
            if hasattr(node, 'start'):
                found = True
                node.start()

        if found == False:
            raise ValueError(f'Could not find a source providing a \'start\' method.')

    def stop(self):
        found = False
        for node in self.__nodes.values():
            if hasattr(node, 'stop'):
                found = True
                node.stop()

        if found == False:
            raise ValueError(f'Could not find a source providing a \'stop\' method.')