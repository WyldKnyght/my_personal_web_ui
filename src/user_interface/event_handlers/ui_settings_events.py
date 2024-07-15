import gradio as gr
from text_generation.character_handler import save_settings

def setup_event_handlers(ui_elements):
    def toggle_dark_mode(current_mode):
        new_mode = 'dark' if current_mode == 'light' else 'light'
        return new_mode

    def save_ui_settings(theme_state):
        # Implement the logic to save the current UI settings
        print("Saving UI settings")
        save_settings(theme_state)

    ui_elements['toggle_dark_mode'].click(
        None, None, None, 
        js='() => {document.getElementsByTagName("body")[0].classList.toggle("dark")}'
    ).then(
        toggle_dark_mode, 
        inputs=[ui_elements['theme_state']], 
        outputs=[ui_elements['theme_state']]
    )

    ui_elements['save_settings_btn'].click(
        save_ui_settings, 
        inputs=[ui_elements['theme_state']], 
        outputs=[]
    )