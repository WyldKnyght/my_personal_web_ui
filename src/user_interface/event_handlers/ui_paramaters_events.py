import gradio as gr
from utils.presets_handler import save_preset, delete_preset, load_preset

def setup_event_handlers(ui_elements):
    def update_peft_visibility(use_peft):
        return {
            ui_elements['lora_r']: gr.update(visible=use_peft),
            ui_elements['lora_alpha']: gr.update(visible=use_peft)
        }

    ui_elements['preset_menu'].change(
        load_preset,
        inputs=[ui_elements['preset_menu']],
        outputs=[ui_elements[key] for key in ui_elements if key not in ['preset_menu', 'save_preset', 'delete_preset']]
    )

    ui_elements['save_preset'].click(
        save_preset,
        inputs=[ui_elements['preset_menu']] + [ui_elements[key] for key in ui_elements if key not in ['preset_menu', 'save_preset', 'delete_preset']],
        outputs=[ui_elements['preset_menu']]
    )

    ui_elements['delete_preset'].click(
        delete_preset,
        inputs=[ui_elements['preset_menu']],
        outputs=[ui_elements['preset_menu']]
    )

    ui_elements['use_peft'].change(
        update_peft_visibility,
        inputs=[ui_elements['use_peft']],
        outputs=[ui_elements['lora_r'], ui_elements['lora_alpha']]
    )

    # Add more event handlers as needed

    return ui_elements