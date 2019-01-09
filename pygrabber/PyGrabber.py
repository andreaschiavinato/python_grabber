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

from pygrabber.dshow_graph import *


class PyGrabber:
    def __init__(self, callback):
        self.graph = FilterGraph()
        self.callback = callback

    def get_devices(self):
        return self.graph.get_input_devices()

    def get_formats(self):
        return self.graph.get_formats()

    def set_device(self, input_device_index):
        self.graph.add_input_device(input_device_index)

    def display_format_dialog(self):
        self.graph.display_format_dialog()

    def start(self, handle):
        self.graph.add_sample_grabber(self.callback)
        self.graph.add_default_render()
        self.graph.prepare()
        self.graph.configure_render(handle)
        self.graph.run()

    def stop(self):
        self.graph.stop()

    def update_window(self, width, height):
        self.graph.update_window(width, height)

    def set_device_properties(self):
        self.graph.set_properties(self.graph.get_input_device())

    def grab_frame(self):
        self.graph.grab_frame()
