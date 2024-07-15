# src\chat_logic\common_handlers\ui_chat_utils.py

from configs import arguments
from utils.history_handlers import validate_mode, save_history

def update_chat_history(state, user_input, assistant_response, unique_id, mode):
    if arguments.args.multi_user:
        return

    # Validate the mode
    mode = validate_mode(mode)

    # Update the in-memory history
    if 'history' not in state:
        state['history'] = {'internal': [], 'visible': []}

    # Add the new exchange to both internal and visible history
    state['history']['internal'].append([user_input, assistant_response])
    state['history']['visible'].append([user_input, assistant_response])

    # Truncate history if it exceeds a certain length (optional)
    max_history_length = 100  # You can adjust this value or make it a parameter
    if len(state['history']['internal']) > max_history_length:
        state['history']['internal'] = state['history']['internal'][-max_history_length:]
        state['history']['visible'] = state['history']['visible'][-max_history_length:]

    # Save the updated history to a file
    save_history(state['history'], unique_id, mode)

    # Return the updated state
    return state