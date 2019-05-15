# The following code captures an image from a camera in a synchronous way.
# An Event object is used to block the main thread until the image is ready.
# The image is shown using matplotlib. Note that the function np.flip is used to invert the last dimension of the image,
# since the image returned by the sample grabber filter has the BGR format, but mathplotlib requires the RGB fromat.

import threading
import matplotlib.pyplot as plt
import numpy as np
from pygrabber.dshow_graph import FilterGraph

image_done = threading.Event()
image_grabbed = None

def img_cb(image):
    global image_done
    global image_grabbed
    image_grabbed = np.flip(image, 2)
    image_done.set()

graph = FilterGraph()
graph.add_video_input_device(0)
graph.add_sample_grabber(img_cb)
graph.add_null_render()
graph.prepare_preview_graph()
graph.run()
input("Press ENTER to grab photo")
graph.grab_frame()
image_done.wait(1000)
graph.stop()
plt.imshow(image_grabbed)
plt.show()

