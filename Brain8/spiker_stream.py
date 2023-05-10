import serial
import matplotlib.pyplot as plt
import numpy as np
from filters import butter_filter

# Constants
BAUDRATE = 230400
INPUT_BUFFER_SIZE = 10000
BUFFER_TO_SECOND = 20000
WINDOW_SIZE = 1 # in seconds

def serialize(port):
    ser = serial.Serial(port=port, baudrate=BAUDRATE, timeout=INPUT_BUFFER_SIZE/BUFFER_TO_SECOND)
    ser.set_buffer_size(rx_size=INPUT_BUFFER_SIZE)
    return ser

def read_arduino(ser):

    data = ser.read(INPUT_BUFFER_SIZE)
    out = [ int(data[i]) for i in range(0, len(data)) ]
    return np.array(out)

def process_data(data):

    data_in = np.array(data)
    result = []

    for i in range(1, len(data_in) - 1):

        if data_in[i] > 127:
            # Found beginning of frame
            # Extract one sample from 2 bytes
            intout = (np.bitwise_and(data_in[i],127))*128
            i = i + 1
            intout = intout + data_in[i]
            result = np.append(result, intout)

    return np.array(result)

def prepare_canvas():

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    plt.ion()
    fig.canvas.draw()

    return fig, ax

def plot_on_canvas(fig, ax, max_time, data, i):
    ax.clear()
    t = np.linspace(0, (i + 1) * INPUT_BUFFER_SIZE / BUFFER_TO_SECOND, len(data))
    ax.plot(t, data)
    plt.xlabel('Time [s]')
    plt.xlim([0, max_time])
    fig.canvas.draw()    
    plt.show()

class Streamer:

    def __init__(self, port, max_time=10):
        self.ser = serialize(port)
        self.max_time = max_time

    def close(self):
        self.ser.close()

    def reserialize(self, port):
        self.close()
        self.ser = serialize(port)

    def set_max_time(self, max_time):
        self.max_time = max_time

    def get_data(self):
        return process_data(read_arduino(self.ser))

    def stream(self, filter=butter_filter):
        
        N_loops = int(BUFFER_TO_SECOND / INPUT_BUFFER_SIZE * self.max_time)
        raw_data = []
        data = []
        fig, ax = prepare_canvas()
        prev_length = 0

        for i in range(N_loops):
            
            # Get data
            raw_data = np.concatenate([raw_data, self.get_data()])

            if i < WINDOW_SIZE * INPUT_BUFFER_SIZE / BUFFER_TO_SECOND:
                continue

            # Filter data
            filtered = filter(raw_data[int(WINDOW_SIZE * INPUT_BUFFER_SIZE / BUFFER_TO_SECOND):])
            data = np.append(data, filtered[prev_length:])
            prev_length = len(filtered)
            plot_on_canvas(fig, ax, self.max_time, data, i)
        
        # plt.plot(np.fft.fftfreq(len(raw_data), 1/10000)[:len(raw_data)//2], np.abs(np.fft.fft(raw_data))[:len(raw_data)//2])
        # plot_on_canvas(fig, ax, self.max_time, raw_data, i)


    def save_data(self, file_path): 
        pass