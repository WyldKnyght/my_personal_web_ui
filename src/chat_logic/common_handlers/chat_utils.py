# src/utils/chat_utils.py

from datetime import datetime

def start_new_chat(state):
    mode = state['mode']
    history = {'internal': [], 'visible': []}

    if mode != 'instruct':
        if greeting := ():
            history['internal'] += [['<|BEGIN-VISIBLE-CHAT|>', greeting]]
            history['visible'] += [['', greeting]]

    unique_id = datetime.now().strftime('%Y%m%d-%H-%M-%S')
    return history, unique_id