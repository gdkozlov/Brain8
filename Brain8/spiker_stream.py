import serial
import matplotlib.pyplot as plt
import numpy as np
import wave
import time
from filters import butter_filter
from stream_handlers import event_handler, game_handler

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
        self.events = []
        self.all_data = []

    def close(self):
        self.ser.close()

    def reserialize(self, port):
        self.close()
        self.ser = serialize(port)

    def set_max_time(self, max_time):
        self.max_time = max_time

    def setup_stream(self):

        # Data collection
        N_loops = int(BUFFER_TO_SECOND / INPUT_BUFFER_SIZE * self.max_time)
        raw_data = []
        data = []
        self.all_data = []

        # Figure
        fig, ax = prepare_canvas()

        return N_loops, raw_data, data, fig, ax

    def get_data(self):
        return process_data(read_arduino(self.ser))
    
    def update_data(self, raw_data, prev_len, filter=butter_filter):

        # Get data
        raw_data = np.concatenate([raw_data, self.get_data()])

        if len(raw_data) >= WINDOW_SIZE * INPUT_BUFFER_SIZE / BUFFER_TO_SECOND:
            
            # Filter data
            filtered_data = filter(raw_data)
            self.all_data = np.append(self.all_data, filtered_data[prev_len:])
            return filtered_data
        
        return []

    def stream(self, filter=butter_filter):
        
        N_loops, raw_data, data, fig, ax = self.setup_stream()
        last_blink_time = 0

        for i in range(N_loops):
            
            # Get the filtered data
            data = self.update_data(raw_data, len(data))

            # Get any events
            events = event_handler(raw_data, data)
            for event in events:
                self.events.append(event)

            # Game input
            game_handler(events, last_blink_time)

            # Plot
            plot_on_canvas(fig, ax, self.max_time, self.all_data, i)

        
        # plt.plot(np.fft.fftfreq(len(raw_data), 1/10000)[:len(raw_data)//2], np.abs(np.fft.fft(raw_data))[:len(raw_data)//2])
        # plot_on_canvas(fig, ax, self.max_time, raw_data, i)

        # uncomment to autosave data
        # with wave.open('data/' + time.strftime("%Y%m%d-%H%M%S"), 'wb') as f:
        #    f.writeframesraw(all_data)


    def save_events(self): 

        for event_data in self.events:
            with wave.open('data/' + time.strftime("%Y%m%d-%H%M%S"), 'wb') as f:
                 f.writeframesraw(event_data)

    def save_data(self): 
        with wave.open('data/' + time.strftime("%Y%m%d-%H%M%S"), 'wb') as f:
            f.writeframesraw(self.all_data)

    def clear_events(self):
        self.events.clear()


######### REPLACE FOR LOOP WITH THIS ONE TO USE THE OLD WORKING CODE

# for i in range(N_loops):
    
#     # Get the data
#     raw_data = np.concatenate([raw_data, self.get_data()])

#     if len(raw_data) < WINDOW_SIZE * INPUT_BUFFER_SIZE / BUFFER_TO_SECOND:
#        continue
    
#     # Filter data
#     filtered_data = filter(raw_data)
#     all_data = np.append(all_data, filtered_data[prev_len:])
#     prev_len = len(filtered_data)  

#     # Get any events
#     if max(data) > EVENT_THRESHOLD and min(data) < -1 * EVENT_THRESHOLD:
#        predicted_sd = predict_movement(data)
#        print(predicted_sd)
#        raw_data.clear()

#        for event in predicted_sd:
#           self.events.append(event)

#     # Plot
#     plot_on_canvas(fig, ax, self.max_time, self.all_data, i)