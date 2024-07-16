# src/user_interface/event_handlers/ui_chat_events.py

import gradio as gr
from chat_logic.common_handlers.start_new_chat import start_new_chat
from chat_logic.reply_handlers.reply_generation import generate_chat_reply, remove_last_message, continue_generation, regenerate_response
from utils.history_handlers import rename_chat, delete_history, load_latest_history
from utils.stopping_event_handler import stop_everything_event
from model_handlers.load_model import load_model
from configs import variables

def setup_event_handlers(ui_elements):
    # Load model
    ui_elements['load_model_btn'].click(
        load_selected_model,
        inputs=[ui_elements['model_selector']],
        outputs=[ui_elements['chat_display']]
    )

    # Chat generation
    ui_elements['generate_btn'].click(
        generate_chat_reply,
        inputs=[ui_elements['chat_input'], ui_elements['chat_history_json'], ui_elements['mode_selector'], ui_elements['chat_style']],
        outputs=[ui_elements['chat_display'], ui_elements['chat_history_json']],
        api_name="chat_api"
    ).then(
        lambda: gr.update(value=""), outputs=[ui_elements['chat_input']]  # Clear the input field after sending
    )

    # Stop generation
    ui_elements['stop_btn'].click(
        stop_everything_event,
        inputs=[],
        outputs=[ui_elements['chat_display']]
    )

    # Continue generation
    ui_elements['continue_btn'].click(
        continue_generation,
        inputs=[ui_elements['chat_history_json'], ui_elements['mode_selector'], ui_elements['chat_style']],
        outputs=[ui_elements['chat_display'], ui_elements['chat_history_json']]
    )

    # Regenerate response
    ui_elements['regenerate_btn'].click(
        regenerate_response,
        inputs=[ui_elements['chat_history_json'], ui_elements['mode_selector'], ui_elements['chat_style']],
        outputs=[ui_elements['chat_display'], ui_elements['chat_history_json']]
    )

    # Remove last message
    ui_elements['remove_last_btn'].click(
        remove_last_message,
        inputs=[ui_elements['chat_history_json']],
        outputs=[ui_elements['chat_display'], ui_elements['chat_history_json']]
    )

    # New chat
    ui_elements['new_chat_btn'].click(
        start_new_chat,
        inputs=[ui_elements['mode_selector']],
        outputs=[ui_elements['chat_display'], ui_elements['chat_history_json'], ui_elements['chat_history']]
    )

    # Rename chat
    ui_elements['rename_chat_btn'].click(
        rename_chat,
        inputs=[ui_elements['chat_history'], gr.Textbox(visible=False), ui_elements['mode_selector']],
        outputs=[ui_elements['chat_history']]
    )

    # Delete chat
    ui_elements['delete_chat_btn'].click(
        delete_history,
        inputs=[ui_elements['chat_history'], ui_elements['mode_selector']],
        outputs=[ui_elements['chat_history'], ui_elements['chat_display'], ui_elements['chat_history_json']]
    )

    # Load selected chat
    ui_elements['chat_history'].change(
        load_latest_history,
        inputs=[ui_elements['mode_selector']],
        outputs=[ui_elements['chat_display'], ui_elements['chat_history_json']]
    )

    # Chat input for sending messages with the Enter key
    ui_elements['chat_input'].submit(
        generate_chat_reply,
        inputs=[ui_elements['chat_input'], ui_elements['chat_history_json'], ui_elements['mode_selector'], ui_elements['chat_style']],
        outputs=[ui_elements['chat_display'], ui_elements['chat_history_json'], ui_elements['chat_input']]
    )
    
def load_selected_model(model_name):
    try:
        model = load_model(model_name)
        variables.model = model
        variables.model_settings = variables.settings.copy()
        return gr.update(value=f"Model '{model_name}' loaded successfully.")
    except Exception as e:
        return gr.update(value=f"Error loading model: {str(e)}")

# Update these functions to work with the GGUF model
for func in [generate_chat_reply, continue_generation, regenerate_response]:
    func.__globals__['model'] = variables.model