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

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os


class ConfigureRecording:
    def __init__(self, parent, audio_devices, video_compressors, audio_compressors, asf_profiles):

        self.filename = StringVar()
        self.filetype = StringVar()
        self.filetype.set(".avi")
        self.audio_device_index = None
        self.video_compressor_index = None
        self.audio_compressor_index = None
        self.asf_profile = None
        self.result = None

        top = self.top = Toplevel(parent)
        top.attributes("-toolwindow", 1)
        top.attributes("-topmost", 1)
        top.geometry("500x290")
        top.resizable(False, False)

        self.lbl_title = Label(top, text='Choose recording options:')
        self.lbl_title.pack(side=TOP, padx=5, pady=5)

        self.content = Frame(top)
        self.content.pack(side=TOP)

        self.lbl_message = Label(top, text='* Valid ony for AVI, ** valid only for WMV')
        self.lbl_message.pack(side=TOP, padx=5, pady=5)

        self.commands = Frame(top)
        self.commands.pack(side=BOTTOM)
        self.commands.columnconfigure(0, weight=1)
        self.commands.columnconfigure(1, weight=1)

        tblen1 = 43
        tblen2 = 50

        self.lbl1 = Label(self.content, text='File name:')
        self.lbl1.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        self.input_file = Entry(master=self.content, width=tblen1,  takefocus=0, textvariable=self.filename)
        self.input_file.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        self.btn_browse = Button(master=self.content, text="Browse", command=self.ask_file_name)
        self.btn_browse.grid(row=0, column=2, padx=5, pady=5)

        self.lbl2 = Label(self.content, text='File type:')
        self.lbl2.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        self.frame_ftype = Frame(self.content)
        self.frame_ftype.grid(row=1, column=1, padx=5, pady=5, sticky=W)
        Radiobutton(self.frame_ftype, text="AVI", variable=self.filetype, value=".avi", command=self.fix_extension).pack(side=LEFT)
        Radiobutton(self.frame_ftype, text="WMV", variable=self.filetype, value=".wmv", command=self.fix_extension).pack(side=LEFT)

        self.lbl3 = Label(self.content, text='Audio device:')
        self.lbl3.grid(row=2, column=0, padx=5, pady=5, sticky=W)

        self.input_audio_device = ttk.Combobox(master=self.content, width=tblen2, values=audio_devices, state='readonly')
        self.input_audio_device.grid(row=2, column=1, padx=5, pady=5, sticky=W, columnspan=2)

        self.lbl4 = Label(self.content, text='Video compressor (*):')
        self.lbl4.grid(row=3, column=0, padx=5, pady=5, sticky=W)

        self.input_video_compressor = ttk.Combobox(master=self.content, width=tblen2, values=video_compressors, state='readonly')
        self.input_video_compressor.grid(row=3, column=1, padx=5, pady=5, sticky=W, columnspan=2)

        self.lbl5 = Label(self.content, text='Audio compressor (*):')
        self.lbl5.grid(row=4, column=0, padx=5, pady=5, sticky=W)

        self.input_audio_compressor = ttk.Combobox(master=self.content, width=tblen2, values=audio_compressors, state='readonly')
        self.input_audio_compressor.grid(row=4, column=1, padx=5, pady=5, sticky=W, columnspan=2)

        self.lbl6 = Label(self.content, text='Windows Media profile (**):')
        self.lbl6.grid(row=5, column=0, padx=5, pady=5, sticky=W)

        self.input_asf_profile = ttk.Combobox(master=self.content, width=tblen2, values=asf_profiles, state='readonly')
        self.input_asf_profile.grid(row=5, column=1, padx=5, pady=5, sticky=W, columnspan=2)

        self.submitButton = Button(self.commands, text='Ok', width=10, command=self.send)
        self.submitButton.grid(row=0, column=0, padx=5, pady=5)

        self.cancelButton = Button(self.commands, text='Cancel', width=10, command=self.cancel)
        self.cancelButton.grid(row=0, column=1, padx=5, pady=5)

    def ask_file_name(self):
        #self.top.withdraw()
        self.top.attributes("-topmost", 0)
        filename = filedialog.asksaveasfilename(
            initialdir="/",
            title="Select file",
            filetypes=[('AVI', ".avi"), ('WMV', ".wmv")])
        #self.top.deiconify()
        self.top.attributes("-topmost", 1)
        if filename is not None:
            filename, file_extension = os.path.splitext(filename)
            if file_extension is not None and file_extension != "":
                self.filetype.set(file_extension)
            self.filename.set(filename)
            self.fix_extension()

    def fix_extension(self):
        filename, file_extension = os.path.splitext(self.filename.get())
        self.filename.set(filename + self.filetype.get())

    def send(self):
        self.audio_device_index = self.input_audio_device.current() if self.input_audio_device.current() >= 0 else None
        self.video_compressor_index = self.input_video_compressor.current() \
            if self.input_video_compressor.current() >= 0 else None
        self.audio_compressor_index = self.input_audio_compressor.current() \
            if self.input_audio_compressor.current() >= 0 else None
        self.asf_profile = self.input_asf_profile.current()
        self.top.destroy()
        self.result = True

    def cancel(self):
        self.top.destroy()
        self.result = False

    def get_audio_device_index(self):
        return self.audio_device_index

    def get_video_compressor_index(self):
        return self.video_compressor_index

    def get_audio_compressor_index(self):
        return self.audio_compressor_index

    def get_filename(self):
        return self.filename.get()

    def get_asf_profile(self):
        return self.input_asf_profile_index
