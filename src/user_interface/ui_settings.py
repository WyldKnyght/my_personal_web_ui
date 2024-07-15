import gradio as gr
from configs import variables
from utils import save_settings

def create_ui():
    with gr.Tab("Settings", elem_id="settings-tab"):
        with gr.Row():
            with gr.Column():
                toggle_dark_mode = gr.Button('Toggle Dark Mode 💡')
                save_settings_btn = gr.Button('Save Settings')

        theme_state = gr.Textbox(visible=False, value='dark' if variables.settings['dark_theme'] else 'light')

        toggle_dark_mode.click(
            None, None, None, 
            js='() => {document.getElementsByTagName("body")[0].classList.toggle("dark")}'
        ).then(
            lambda x: 'dark' if x == 'light' else 'light', 
            theme_state, 
            theme_state
        )

        save_settings_btn.click(
            save_settings, 
            inputs=[theme_state], 
            outputs=[]
        )

    return {
        'toggle_dark_mode': toggle_dark_mode,
        'save_settings_btn': save_settings_btn,
        'theme_state': theme_state
    }