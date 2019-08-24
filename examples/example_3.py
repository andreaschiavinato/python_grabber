# The following code uses the sample grabber filter to capture single images from the camera.
# To capture an image, the method grab_frame is called. The image will be retrieved from the callback function passed
# as parameter to the add_sample_grabber method. In this case, the image captured is shown using the function
# imshow of opencv.

from pygrabber.dshow_graph import FilterGraph
import cv2

graph = FilterGraph()
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
graph.add_video_input_device(0)
graph.add_sample_grabber(lambda image: cv2.imshow("Image", image))
graph.add_null_render()
graph.prepare_preview_graph()
graph.run()
print("Press 'C' or 'c' to grab photo, another key to exit")
while cv2.waitKey(0) in [ord('c'), ord('C')]:
    graph.grab_frame()
graph.stop()
cv2.destroyAllWindows()
print("Done")