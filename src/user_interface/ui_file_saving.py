# /user_interface/ui_file_saving.py
import gradio as gr

def create_ui():
    with gr.Group(visible=False, elem_classes='file-saver') as file_saver:
        save_filename = gr.Textbox(lines=1, label='File name')
        save_root = gr.Textbox(lines=1, label='File folder', info='For reference. Unchangeable.', interactive=False)
        save_contents = gr.Textbox(lines=10, label='File contents')
        with gr.Row():
            save_cancel = gr.Button('Cancel', elem_classes="small-button")
            save_confirm = gr.Button('Save', elem_classes="small-button", variant='primary')

    with gr.Group(visible=False, elem_classes='file-saver') as file_deleter:
        delete_filename = gr.Textbox(lines=1, label='File name')
        delete_root = gr.Textbox(lines=1, label='File folder', info='For reference. Unchangeable.', interactive=False)
        with gr.Row():
            delete_cancel = gr.Button('Cancel', elem_classes="small-button")
            delete_confirm = gr.Button('Delete', elem_classes="small-button", variant='stop')

    with gr.Group(visible=False, elem_classes='file-saver') as preset_saver:
        save_preset_filename = gr.Textbox(lines=1, label='File name', info='The preset will be saved to your presets/ folder with this base filename.')
        save_preset_contents = gr.Textbox(lines=10, label='File contents')
        with gr.Row():
            save_preset_cancel = gr.Button('Cancel', elem_classes="small-button")
            save_preset_confirm = gr.Button('Save', elem_classes="small-button", variant='primary')

    return {
        'file_saver': file_saver,
        'save_filename': save_filename,
        'save_root': save_root,
        'save_contents': save_contents,
        'save_cancel': save_cancel,
        'save_confirm': save_confirm,
        'file_deleter': file_deleter,
        'delete_filename': delete_filename,
        'delete_root': delete_root,
        'delete_cancel': delete_cancel,
        'delete_confirm': delete_confirm,
        'preset_saver': preset_saver,
        'save_preset_filename': save_preset_filename,
        'save_preset_contents': save_preset_contents,
        'save_preset_cancel': save_preset_cancel,
        'save_preset_confirm': save_preset_confirm
    }