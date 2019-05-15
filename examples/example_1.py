# This code lists the cameras connected to your PC:

from pygrabber.dshow_graph import FilterGraph

graph = FilterGraph()
print(graph.get_input_devices())