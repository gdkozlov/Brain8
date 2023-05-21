import time
from pynput.keyboard import Key, Controller
from event_classifier import predict_movement

# I found 15-30ish to be good
EVENT_THRESHOLD = 30

def is_event(data):
    return max(data) > EVENT_THRESHOLD and min(data) < -1 * EVENT_THRESHOLD

def event_handler(raw_data, data):

    if len(data) == 0:
        return []

    if is_event(data):
        print('event')
        predicted_sd = predict_movement(data)
        print(predicted_sd)
        raw_data.clear()

        return predicted_sd
    
    return []

def input_handler(event, last_blink_time):

    keyboard = Controller()
    is_pressed = False

    if event is None:
        return last_blink_time, is_pressed

    if event == 'L':
        keyboard.press(Key.left)
        keyboard.release(Key.left)
        is_pressed = True

    elif event == 'R':
        keyboard.press(Key.right)
        keyboard.release(Key.right)
        is_pressed = True

    # Event must be a blink here onwards
    elif time.time() - last_blink_time < 5:
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        last_blink_time = 0
        is_pressed = True

    else:
        last_blink_time = time.time()


    return last_blink_time, is_pressed


def game_handler(events, last_blink_time):
    
    if not events:
        return last_blink_time 
    
    for event in events:
        last_blink_time = input_handler(event, last_blink_time)

    return last_blink_time 