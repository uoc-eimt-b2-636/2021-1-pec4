# -*- coding: utf-8 -*-

import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore");

import sys
import signal
import threading
import time
import logging
import math
import collections
import numpy as np

import FFTPlotter

import pyaudio
import wave

is_finished = False
fft_plotter = None
plot_event = None

def pyaudio_callback(in_data, frame_count, time_info, status):
    global fft_plotter
    global plot_event

    audio_samples = np.fromstring(in_data, dtype=np.int16)

    fft_plotter.set_data(audio_samples)
    plot_event.set()

    return (in_data, pyaudio.paContinue)

def signal_handler(signal, frame):
    global is_finished
    print "Detectado CTRL + C!"
    is_finished = True

def main():
    global is_finished
    global fft_plotter
    global plot_event

    # Get logger class
    log = logging.getLogger("Main")

    # Create signal handler event
    signal.signal(signal.SIGINT, signal_handler)

    # Create asynchronous events
    plot_event = threading.Event()

    # Clear events
    plot_event.clear()

    # Create threads
    fft_plotter = FFTPlotter.FFTPlotter(event = plot_event)

    # Start threads
    fft_plotter.start()

    # Init Pyaudio
    p = pyaudio.PyAudio()

    # Open audio stream
    stream = p.open(format = pyaudio.paInt16,
                    channels = 2,
                    rate = 22050,
                    input = True,
                    output = False,
                    frames_per_buffer = 1024*8,
                    stream_callback = pyaudio_callback)

    # Init audio stream
    stream.start_stream()

    print "Presione CTRL+C para parar!"

    log.debug("Starting...")

    # Until program is not finished
    while (not is_finished):
        time.sleep(.01)

    log.debug("Finishing...")

    fft_plotter.exit()

    fft_plotter.join()

    log.debug("Finished")

    # Close audio stream
    stream.stop_stream()
    stream.close()

    # Terminate Pyaudio
    p.terminate()

# Entry point, main function
if __name__ == '__main__':
    logging.basicConfig(level=logging.NOTSET,
                        filename='capturar.log', filemode='w+',
                        format='%(name)s %(levelname)s %(message)s')

    # Main call
    main()
