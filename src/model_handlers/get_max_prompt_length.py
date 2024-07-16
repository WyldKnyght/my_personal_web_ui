# src\chat_logic\prompt_handlers\get_max_prompt_length.py

def get_max_prompt_length(state):
    return state['truncation_length'] - state['max_new_tokens']
