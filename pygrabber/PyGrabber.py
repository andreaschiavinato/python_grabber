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
        self.preview_graph_prepared = False
        self.recording_prepared = False

    def get_video_devices(self):
        return self.graph.get_input_devices()

    def get_audio_devices(self):
        return self.graph.get_audio_devices()

    def get_video_compressors(self):
        return self.graph.get_video_compressors()

    def get_audio_compressors(self):
        return self.graph.get_audio_compressors()

    def get_asf_profiles(self):
        return self.graph.get_asf_profiles()

    def set_device(self, input_device_index):
        self.graph.add_video_input_device(input_device_index)

    def start_preview(self, handle):
        if not self.preview_graph_prepared:
            if self.recording_prepared:
                self.graph.remove_all_filters_but_video_source()
                self.recording_prepared = False

            self.graph.add_sample_grabber(self.callback)
            self.graph.add_default_render()
            self.graph.prepare_preview_graph()
            self.graph.configure_render(handle)
            self.preview_graph_prepared = True
        self.graph.run()

    def start_recording(self, audio_device_index, video_compressor_index, audio_compressor_index, filename, handle):
        self.graph.stop()
        self.preview_graph_prepared = False
        self.graph.remove_all_filters_but_video_source()
        self.graph.add_default_render()
        if video_compressor_index is not None:
            self.graph.add_video_compressor(video_compressor_index)
        if audio_device_index is not None:
            self.graph.add_audio_input_device(audio_device_index)
            if audio_compressor_index is not None:
                self.graph.add_audio_compressor(audio_compressor_index)
        self.graph.add_file_writer_and_muxer(filename)
        self.graph.prepare_recording_graph()
        self.graph.configure_render(handle)
        self.recording_prepared = True
        self.graph.run()

    def stop(self):
        self.graph.stop()

    def update_window(self, width, height):
        self.graph.update_window(width, height)

    def set_device_properties(self):
        self.graph.get_input_device().set_properties()

    def display_format_dialog(self):
        self.graph.get_input_device().show_format_dialog()

    def grab_frame(self):
        self.graph.grab_frame()

    def get_status(self):
        graph_state = self.graph.get_state()
        device_name = self.graph.get_input_device().Name
        resolution = self.graph.get_input_device().get_current_format()
        if graph_state == StateGraph.Stopped:
            return "Stopped"
        elif graph_state == StateGraph.Running:
            return f"{'Recording' if self.graph.is_recording else 'Playing'} {device_name} [{resolution[0]}x{resolution[1]}]"
        elif graph_state == StateGraph.Paused:
            return f"Connected to {device_name} - paused"
        return None
