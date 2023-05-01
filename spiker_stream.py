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

def plot_on_canvas(fig, ax, t, data, max_time):
    ax.clear()
    ax.plot(t, data)
    plt.xlabel('Time [s]')
    plt.xlim([0, max_time])
    fig.canvas.draw()    
    plt.show()

class Streamer:

    def __init__(self, port, max_time=10):
        self.ser = serialize(port)
        self.max_time = max_time

    def reserialize(self, port):
        self.ser.close()
        self.ser = serialize(port)

    def set_max_time(self, max_time):
        self.max_time = max_time

    def stream(self, filter=lambda x:x):

        N_loops = int(BUFFER_TO_SECOND / INPUT_BUFFER_SIZE * self.max_time)
        fig, ax = prepare_canvas()

        for i in range(N_loops):
                
            # Get data
            raw_data = read_arduino(self.ser)
            data_temp = process_data(raw_data)
            
            unfiltered_data = np.append(data_temp, unfiltered_data) if i != 0 else np.array(data_temp)

            # filtered_data = filter(unfiltered_data)

            t = np.linspace(0, (i + 1) * INPUT_BUFFER_SIZE / BUFFER_TO_SECOND, len(unfiltered_data))

            plot_on_canvas(fig, ax, t, unfiltered_data, self.max_time)

    def save_data(self, file_path): 
        pass




 