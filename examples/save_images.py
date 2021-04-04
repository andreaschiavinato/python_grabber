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
