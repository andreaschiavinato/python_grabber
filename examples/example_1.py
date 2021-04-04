# This code lists the cameras connected to your PC:

from pygrabber.dshow_graph import FilterGraph

if __name__ == "__main__":
    graph = FilterGraph()
    print(graph.get_input_devices())