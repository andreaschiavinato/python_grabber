# The following code connect to the first capture device, list all the available formats, then allows you to pick one.
# After selecting a format the live video from the camera is shown.

from pygrabber.dshow_graph import FilterGraph
from tkinter import Tk


if __name__ == "__main__":
    graph = FilterGraph()
    graph.add_video_input_device(0)
    formats = graph.get_input_device().get_formats()
    print(f"Available formats for {graph.get_input_device().Name}")
    for f in formats:
        print(f)
    format_id = input("Enter a format id: ")
    graph.get_input_device().set_format(int(format_id))
    graph.add_default_render()
    graph.prepare_preview_graph()
    graph.run()
    root = Tk()
    root.withdraw() # hide Tkinter main window
    root.mainloop()
