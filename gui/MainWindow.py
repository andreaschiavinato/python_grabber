#
# python_grabber
#
# Authors:
#  Andrea Schiavinato <andrea.schiavinato84@gmail.com>
#
# Copyright (C) 2019 Andrea Schiavinato
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import queue
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog

from gui.SelectDevice import *
from gui.ConfigureRecording import *
from pygrabber.PyGrabber import *
from pygrabber.image_process import *


class MainWindow:
    def __init__(self, master):
        self.create_gui(master)
        self.grabber = PyGrabber(self.on_image_received)
        self.queue = queue.Queue()
        self.image = None
        self.original_image = None
        self.select_device()

    def create_gui(self, master):
        self.master = master
        master.title("Python Photo App")
        self.create_menu(master)

        master.columnconfigure(0, weight=1, uniform="group1")
        master.columnconfigure(1, weight=1, uniform="group1")
        master.rowconfigure(0, weight=1)

        self.video_area = Frame(master, bg='black')
        self.video_area.grid(row=0, column=0, sticky=W+E+N+S, padx=5, pady=5)

        self.status_area = Frame(master)
        self.status_area.grid(row=1, column=0, sticky=W+E+N+S, padx=5, pady=5)

        self.image_area = Frame(master)
        self.image_area.grid(row=0, column=1, sticky=W+E+N+S, padx=5, pady=5)

        self.image_controls_area = Frame(master)
        self.image_controls_area.grid(row=1, column=1, padx=5, pady=0)

        self.image_controls_area2 = Frame(master)
        self.image_controls_area2.grid(row=2, column=1, padx=5, pady=0)

        # Grabbed image
        fig = Figure(figsize=(5, 4), dpi=100)
        self.plot = fig.add_subplot(111)
        self.plot.axis('off')

        self.canvas = FigureCanvasTkAgg(fig, master=self.image_area)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=1)

        # Status
        self.lbl_status1 = Label(self.status_area, text="No device selected")
        self.lbl_status1.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        # Image controls
        self.grab_btn = Button(self.image_controls_area, text="Grab", command=self.grab_frame)
        self.grab_btn.pack(padx=5, pady=20, side=LEFT)

        self.image_filter_orig_btn = Button(self.image_controls_area, text="Original", command=self.restore_original_image)
        self.image_filter_orig_btn.pack(padx=5, pady=2, side=LEFT)

        self.image_filter_1_btn = Button(self.image_controls_area, text="Sepia", command=self.image_filter(sepia))
        self.image_filter_1_btn.pack(padx=5, pady=2, side=LEFT)

        self.image_filter_2_btn = Button(self.image_controls_area, text="Edge Preserving", command=self.image_filter(edge_preserving))
        self.image_filter_2_btn.pack(padx=5, pady=2, side=LEFT)

        self.image_filter_3_btn = Button(self.image_controls_area2, text="Stylization", command=self.image_filter(stylization))
        self.image_filter_3_btn.pack(padx=5, pady=2, side=LEFT)

        self.image_filter_4_btn = Button(self.image_controls_area2, text="Pencil Sketch", command=self.image_filter(pencil_sketch))
        self.image_filter_4_btn.pack(padx=5, pady=2, side=LEFT)

        self.save_btn = Button(self.image_controls_area2, text="Save", command=self.save_image)
        self.save_btn.pack(padx=5, pady=2, side=LEFT)

        self.video_area.bind("<Configure>", self.on_resize)

    def create_menu(self, master):
        menubar = Menu(master)
        self.master.config(menu=menubar)

        camera_menu = Menu(menubar)
        camera_menu.add_command(label="Open...", command=self.change_camera)
        camera_menu.add_command(label="Set properties...", command=self.camera_properties)
        camera_menu.add_command(label="Set format...", command=self.set_format)
        camera_menu.add_command(label="Start preview", command=self.start_preview)
        camera_menu.add_command(label="Stop", command=self.stop)
        menubar.add_cascade(label="Camera", menu=camera_menu)

        image_menu = Menu(menubar)
        image_menu.add_command(label="Grab image", command=self.grab_frame)
        image_menu.add_command(label="Save...", command=self.save_image)
        menubar.add_cascade(label="Image", menu=image_menu)

        recording_menu = Menu(menubar)
        recording_menu.add_command(label="Start recording...", command=self.start_stop_recording)
        recording_menu.add_command(label="Stop recording", command=self.stop)
        menubar.add_cascade(label="Video Recording", menu=recording_menu)

    def display_image(self):
        while self.queue.qsize():
            try:
                self.image = self.queue.get(0)
                self.original_image = self.image
                self.plot.imshow(np.flip(self.image, axis=2))
                self.canvas.draw()
            except queue.Empty:
                pass
        self.master.after(100, self.display_image)

    def select_device(self):
        input_dialog = SelectDevice(self.master, self.grabber.get_video_devices())
        self.master.wait_window(input_dialog.top)
        # no device selected
        if input_dialog.device_id is None:
            exit()

        self.grabber.set_device(input_dialog.device_id)
        self.grabber.start_preview(self.video_area.winfo_id())
        self.display_status(self.grabber.get_status())
        self.on_resize(None)
        self.display_image()

    def display_status(self, status):
        self.lbl_status1.config(text=status)

    def change_camera(self):
        self.grabber.stop()
        del self.grabber
        self.grabber = PyGrabber(self.on_image_received)
        self.select_device()

    def camera_properties(self):
        self.grabber.set_device_properties()

    def set_format(self):
        self.grabber.display_format_dialog()

    def on_resize(self, event):
        self.grabber.update_window(self.video_area.winfo_width(), self.video_area.winfo_height())

    def init_device(self):
        self.grabber.start()

    def grab_frame(self):
        self.grabber.grab_frame()

    def start_stop_recording(self):
        audio_devices = self.grabber.get_audio_devices()
        video_compressors = self.grabber.get_video_compressors()
        audio_compressors = self.grabber.get_audio_compressors()
        asf_profiles = self.grabber.get_asf_profiles()
        input_dialog = ConfigureRecording(self.master, audio_devices, video_compressors, audio_compressors, asf_profiles)
        self.master.wait_window(input_dialog.top)
        if input_dialog.result:
            try:
                self.grabber.start_recording(input_dialog.get_audio_device_index(),
                                             input_dialog.get_video_compressor_index(),
                                             input_dialog.get_audio_compressor_index(),
                                             input_dialog.get_filename(),
                                             self.video_area.winfo_id())
                self.grabber.update_window(self.video_area.winfo_width(), self.video_area.winfo_height())
                self.display_status(self.grabber.get_status())
            except:
                messagebox.showinfo("Error", "An error occurred during the recoding. Select a different comnination of compressors and try again.")
                self.display_status(self.grabber.get_status())

    def on_image_received(self, image):
        self.queue.put(image)

    def start_preview(self):
        self.grabber.start_preview(self.video_area.winfo_id())
        self.display_status(self.grabber.get_status())
        self.on_resize(None)

    def stop(self):
        self.grabber.stop()
        self.display_status(self.grabber.get_status())

    def save_image(self):
        filename = filedialog.asksaveasfilename(
            initialdir="/",
            title="Select file",
            filetypes=[('PNG', ".png"), ('JPG', ".jpg")])
        if filename is not None:
            save_image(filename, self.image)

    def image_filter(self, process_function):
        def inner():
            if self.original_image is None:
                return
            self.image = process_function(self.original_image)
            self.plot.imshow(np.flip(self.image, axis=2))
            self.canvas.draw()
        return inner

    def restore_original_image(self):
        if self.original_image is None:
            return
        self.image = self.original_image
        self.plot.imshow(np.flip(self.image, axis=2))
        self.canvas.draw()
