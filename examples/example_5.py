# The following code is an improvement of Example 4 that allows you to capture images from two camera at the same time.

import threading
import matplotlib.pyplot as plt
import numpy as np
from pygrabber.dshow_graph import FilterGraph


class Camera:
    def __init__(self, device_id):
        self.graph = FilterGraph()
        self.graph.add_video_input_device(device_id)
        self.graph.add_sample_grabber(self.img_cb)
        self.graph.add_null_render()
        self.graph.get_input_device().set_format()
        self.graph.prepare_preview_graph()
        self.graph.run()

        self.image_grabbed = None
        self.image_done = threading.Event()

    def img_cb(self, image):
        self.image_grabbed = np.flip(image, 2)
        self.image_done.set()

    def capture(self):
        self.graph.grab_frame()

    def wait_image(self):
        self.image_done.wait(1000)
        return self.image_grabbed


print("Opening first camera")
camera1 = Camera(0)
print("Opening second camera")
camera2 = Camera(1)
input("Press ENTER to grab photos")
camera1.capture()
camera2.capture()
print("Waiting images")
image1 = camera1.wait_image()
image2 = camera2.wait_image()
print("Done")
ax1 = plt.subplot(2, 1, 1)
ax1.imshow(image1)
ax2 = plt.subplot(2, 1, 2)
ax2.imshow(image2)
plt.show()
