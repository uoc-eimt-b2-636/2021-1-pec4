# -*- coding: utf-8 -*-

import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore");
    import matplotlib.pyplot as plt

import sys
import threading
import collections
import struct
import logging
import time

from matplotlib import colors
from matplotlib.colors import LogNorm

import numpy as np

# Normalize numpy array in range [-1, 1]
def normalize11(a):
    r = a - np.min(a)
    r = r / np.max(r)
    r = (r - .5) * 2
    
    return r

class FFTPlotter(threading.Thread):
    def __init__(self, event = None):
        threading.Thread.__init__(self)

        self.event = event

        self.log = logging.getLogger("FFTPlotter")

        self.data = None

        self.is_finished = False

    def exit(self):
        self.log.debug("Exitting")
        self.is_finished = True

    def run(self):
        self.log.debug("Starting")

        fig = plt.figure(figsize=(12, 9))

        plt.ion()
        fig.show(False)

        # Two subplots, unpack the axis array immediately
        ax1 = fig.add_subplot(2,1,1)
        ax2 = fig.add_subplot(2,1,2)

        fig.show()
        fig.canvas.draw()

        while not self.is_finished:
            # Wait for image to be received or timeout
            if self.event.wait(0.001):
                self.event.clear()

                ax1.clear()
                ax1.set_title("Microphone Samples")
                ax1.set_ylabel("Audio Amplitude")
                ax1.set_xlabel("Time Sample Id")
                ax1.grid(True)

                ax2.clear()
                ax2.set_title("Microphone FFT")
                ax2.set_ylabel("FFT Magnitude")
                ax2.set_xlabel("Frequency (kHz)")
                ax2.grid(True)

                values = np.asarray(self.data, dtype=np.float)

                # Some scaling or normalization
                # values = values / 10000
                values = normalize11(values)

                data_fft = abs(np.fft.fft(values)) / len(values)
                data_fft = np.fft.fftshift(data_fft)
                data_fft = data_fft[0:4096]

                # BW = 22050 / 2
                freq_axis = np.true_divide(np.arange(0, 4096), 4096) * 22050 / 2 / 1000

                ax1.set_ylim([-1.3, 1.3])
                ax1.set_xlim([0, 8192])
                ax1.plot(values, lw=1, color="k")

                ax2.set_ylim([-60, 0])
                ax2.plot(freq_axis, 10*np.log10(data_fft), lw=1, color="darkred")

                fig.canvas.draw()
                fig.canvas.flush_events()

        plt.ioff()
        plt.close()

        self.log.debug("Exited")


    def set_data(self, data):
        self.data = data
