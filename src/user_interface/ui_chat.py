import gradio as gr
from chat_logic.common_handlers.get_available_chat_styles import get_available_chat_styles
from chat_logic.prompt_handlers.get_available_prompts import get_available_prompts

def create_ui():
    with gr.Tab('Chat', elem_id='chat-tab'):
        with gr.Row():
            with gr.Column(scale=3):
                chat_display = gr.HTML(elem_id='chat-display')
                
                with gr.Row():
                    chat_input = gr.Textbox(label='', placeholder='Send a message', elem_id='chat-input', elem_classes=['add_scrollbar'])
                
                with gr.Row():
                    generate_btn = gr.Button('Generate', elem_id='generate-btn', variant='primary')
                    stop_btn = gr.Button('Stop', elem_id='stop-btn')
                    continue_btn = gr.Button('Continue', elem_id='continue-btn')
                
                with gr.Row():
                    regenerate_btn = gr.Button('Regenerate', elem_id='regenerate-btn')
                    remove_last_btn = gr.Button('Remove last reply', elem_id='remove-last-btn')
                
                with gr.Row():
                    mode_selector = gr.Radio(choices=['chat', 'chat-instruct', 'instruct'], label='Mode', value='chat', elem_id='mode-selector')
                    chat_style = gr.Dropdown(choices=get_available_chat_styles(), label='Chat style', value='cai-chat', elem_id='chat-style')

            with gr.Column(scale=1):
                with gr.Row():
                    new_chat_btn = gr.Button('New chat', elem_id='new-chat-btn')
                
                gr.Markdown("Past chats")
                chat_history = gr.Radio(label="", elem_classes=['slim-dropdown'], elem_id='past-chats')
                
                with gr.Row():
                    rename_chat_btn = gr.Button('Rename', elem_classes='refresh-button', elem_id='rename-chat-btn')
                    delete_chat_btn = gr.Button('🗑️', elem_classes='refresh-button', elem_id='delete-chat-btn')
                
                gr.Markdown("Prompts")
                prompt_menu = gr.Dropdown(choices=get_available_prompts(), value='None', label='Prompt', elem_classes='slim-dropdown', elem_id='prompt-menu')
                refresh_prompts_btn = gr.Button('🔄', elem_classes='refresh-button', elem_id='refresh-prompts-btn')

    chat_history_json = gr.JSON(visible=False, elem_id='chat-history-json')

    return {
        'chat_display': chat_display,
        'chat_input': chat_input,
        'generate_btn': generate_btn,
        'stop_btn': stop_btn,
        'continue_btn': continue_btn,
        'regenerate_btn': regenerate_btn,
        'remove_last_btn': remove_last_btn,
        'mode_selector': mode_selector,
        'chat_style': chat_style,
        'new_chat_btn': new_chat_btn,
        'chat_history': chat_history,
        'rename_chat_btn': rename_chat_btn,
        'delete_chat_btn': delete_chat_btn,
        'prompt_menu': prompt_menu,
        'refresh_prompts_btn': refresh_prompts_btn,
        'chat_history_json': chat_history_json
    }