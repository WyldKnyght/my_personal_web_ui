# src/utils/chat_utils.py

from datetime import datetime
from configs import variables

def start_new_chat(state):
    mode = state['mode']
    history = {'internal': [], 'visible': []}

    if mode != 'instruct':
        if greeting := variables.get_setting('greeting', ''):
            history['internal'] += [['<|BEGIN-VISIBLE-CHAT|>', greeting]]
            history['visible'] += [['', greeting]]

    unique_id = datetime.now().strftime('%Y%m%d-%H-%M-%S')
    return history, unique_id