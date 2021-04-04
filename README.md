# python_grabber
This is a Python library that enables you to use video cameras from Python on Windows. It is based on DirectShow.
In particular, it allows to:
 * Capture photos from a video camera
 * View installed cameras on a system
 * Set the camera options
 * Save a vide captured from a camera

The library is available on PyPI: https://pypi.org/project/pygrabber/0.1/

## Basic example
```python
# This code lists the cameras connected to your PC:

from pygrabber.dshow_graph import FilterGraph

graph = FilterGraph()
print(graph.get_input_devices())
```

## Save images example
```python

# Captures a frame from the first camera found on your computer every second and saves it to a file

import cv2
from datetime              import datetime
from threading             import Event, Thread
from pygrabber.dshow_graph import FilterGraph
from os                    import path

PAUSE_BETWEEN_CAPTURE = 1  # 1 sec.
OUTPUT_FOLDER         = r"C:\test\\"
CAMERA_INDEX          = 0 # Using first camera found

global start_time


def capture_photos_loop(event_):
    global start_time
    start_time = datetime.now()
    while not event_.isSet():
        graph.grab_frame()
        event_.wait(PAUSE_BETWEEN_CAPTURE)


def show_image(image):
    global start_time
    capture_time = datetime.now() - start_time
    image_file_name = path.join(OUTPUT_FOLDER, str(capture_time.seconds * 1000 + int(capture_time.microseconds / 1000)) + ".jpg")
    cv2.imwrite(image_file_name, image)
    print(f"Image {image_file_name} written")


if __name__ == "__main__":
    event          = Event()
    capture_thread = Thread(target=capture_photos_loop, args=(event, ))
    graph          = FilterGraph()
    devices        = graph.get_input_devices()

    print(f"Connecting to device {devices[CAMERA_INDEX]}")
    graph.add_video_input_device(CAMERA_INDEX)
    graph.add_sample_grabber(lambda image: show_image(image))
    graph.add_null_render()
    graph.prepare_preview_graph()
    graph.run()

    capture_thread.start()
    input(f"Capturing images every {PAUSE_BETWEEN_CAPTURE}s, press ENTER to terminate.")
    event.set()
    capture_thread.join()
    print("Done")
```
## View live video example
```python
# This code shows a screen with the live image from the first camera in your PC.
# We add to the graph two filters: one is a source filter corresponding to the first camera connected to your PC,
# the second is the default render, that shows the images from the camera in a window on the screen.
# Then we call prepare, that connects the two filters together, and run, to execute the graph.
# Finally, we need a method to pause the program while watching the camera video.
# I use the Tkinter mainloop function which fetches and handles Windows events, so the application does't seem frozen.

from pygrabber.dshow_graph import FilterGraph
from tkinter               import Tk

graph = FilterGraph()
graph.add_video_input_device(0)
graph.add_default_render()
graph.prepare_preview_graph()
graph.run()
root = Tk()
root.withdraw() # hide Tkinter main window
root.mainloop()
```

See also the other examples on the "examples" folder and the article https://www.codeproject.com/Articles/1274094/%2FArticles%2F1274094%2FCapturing-images-from-camera-using-Python-and-Dire.

## Sample GUI application

The file run_gui.py will run a tool with a GUI that enables you to use a camera connected to your system, capture still frames or videos, do basic image porcessing. 
