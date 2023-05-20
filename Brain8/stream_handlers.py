import time
from pynput.keyboard import Key, Controller
from event_classifier import predict_movement

# I found 15-30ish to be good
EVENT_THRESHOLD = 15

def is_event(data):
    return max(data) > EVENT_THRESHOLD and min(data) < -1 * EVENT_THRESHOLD

def event_handler(raw_data, data):

    if not data:
        return []

    if is_event(data):
        predicted_sd = predict_movement(data)
        print(predicted_sd)
        raw_data.clear()

        return predicted_sd
    
    return []

def input_handler(event, last_blink_time):

    keyboard = Controller()

    if event is None:
        return last_blink_time

    if event == 'L':
        keyboard.press('a')
        keyboard.release('a')
        print("a pressed")

    elif event == 'R':
        keyboard.press('d')
        keyboard.release('d')
        print("d pressed")

    # Event must be a blink here onwards
    elif time.time() - last_blink_time < 0.5:
        keyboard.press('s')
        keyboard.release('s')
        print("s pressed")
    
    else:
        last_blink_time = time.time()

    return last_blink_time


def game_handler(events, last_blink_time):
    
    if not events:
        return last_blink_time 
    
    for event in events:
        last_blink_time = input_handler(event, last_blink_time)

    return last_blink_time 