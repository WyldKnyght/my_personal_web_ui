# src\user_interface\event_handlers\ui_chat_events.py 
import gradio as gr
from chat_logic.prompt_handlers.get_available_prompts import get_available_prompts
from chat_logic.reply_handlers.generate_chat_reply import generate_chat_reply
from chat_logic.reply_handlers.remove_last_message import remove_last_message
from chat_logic.common_handlers.start_new_chat import start_new_chat
from utils.history_handlers import rename_history, delete_history
from utils.stopping_event_handler import stop_everything_event
from utils.continue_generation import continue_generation
from chat_logic.reply_handlers.regenerate_response import regenerate_response
from chat_logic.common_handlers.update_chat_history import update_chat_history
from chat_logic.prompt_handlers.load_prompt import load_prompt

def setup_event_handlers(ui_elements):
    # Chat generation
    ui_elements['generate_btn'].click(
        generate_chat_reply,
        inputs=[ui_elements['chat_input'], ui_elements['chat_history_json'], ui_elements['mode_selector'], ui_elements['chat_style']],
        outputs=[ui_elements['chat_display'], ui_elements['chat_history_json']]
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
        inputs=[],
        outputs=[ui_elements['chat_display'], ui_elements['chat_history_json'], ui_elements['chat_history']]
    )

    # Rename chat
    ui_elements['rename_chat_btn'].click(
        rename_history,
        inputs=[ui_elements['chat_history'], gr.Textbox(visible=False)],  # You might want to add a visible textbox for the new name
        outputs=[ui_elements['chat_history']]
    )

    # Delete chat
    ui_elements['delete_chat_btn'].click(
        delete_history,
        inputs=[ui_elements['chat_history']],
        outputs=[ui_elements['chat_history'], ui_elements['chat_display'], ui_elements['chat_history_json']]
    )

    # Load selected chat
    ui_elements['chat_history'].change(
        update_chat_history,
        inputs=[ui_elements['chat_history']],
        outputs=[ui_elements['chat_display'], ui_elements['chat_history_json']]
    )

    # Load selected prompt
    ui_elements['prompt_menu'].change(
        load_prompt,
        inputs=[ui_elements['prompt_menu']],
        outputs=[ui_elements['chat_input']]
    )

    # Refresh prompts
    ui_elements['refresh_prompts_btn'].click(
        lambda: gr.update(choices=get_available_prompts()),
        inputs=[],
        outputs=[ui_elements['prompt_menu']]
    )

    # You might also want to add a handler for the chat input for sending messages with the Enter key
    ui_elements['chat_input'].submit(
        generate_chat_reply,
        inputs=[ui_elements['chat_input'], ui_elements['chat_history_json'], ui_elements['mode_selector'], ui_elements['chat_style']],
        outputs=[ui_elements['chat_display'], ui_elements['chat_history_json'], ui_elements['chat_input']]
    )