# IOIOCore

IOIOCore is general purpose data propagation framework for realtime applications written in python.

# Node
A node is a individual unit or component that performs a specific task in a larger system. Each node typically has inputs, outputs, and processing logic that transforms data as it moves through the system. Nodes are interconnected to form a pipeline where the output of one node becomes the input of another, enabling complex workflows or data transformations.

## Input and Output Ports
Nodes receive data through input ports and send processed data out through output ports. The number and type of ports may vary depending on the node's purpose.

## Processing Logic
Each node contains specific logic or algorithms to process the data it receives. This could range from basic transformations (like filtering or mapping) to more complex operations (like aggregation or machine learning inference).

Create specific nodes by deriving from the Node parent class. Define input and output ports and implement the processing logic for child objects.

# Sources

TBD

# Pipeline

TBD