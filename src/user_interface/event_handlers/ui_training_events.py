# training_event_handlers.py

import gradio as gr
from utils.file_manager import get_datasets
from modules.train_lora import train_lora

def setup_event_handlers(ui_elements):
    def start_training(lora_name, lora_rank, lora_alpha, batch_size, learning_rate, epochs, cutoff_len, dataset, eval_dataset, format, eval_steps):
        # This function should implement the actual training logic
        # For now, we'll just return a placeholder message
        return f"Starting training for LoRA: {lora_name}"

    def interrupt_training():
        # This function should implement the logic to interrupt the training
        # For now, we'll just return a placeholder message
        return "Training interrupted"

    ui_elements['start_button'].click(
        start_training,
        inputs=[
            ui_elements['lora_name'],
            ui_elements['lora_rank'],
            ui_elements['lora_alpha'],
            ui_elements['batch_size'],
            ui_elements['learning_rate'],
            ui_elements['epochs'],
            ui_elements['cutoff_len'],
            ui_elements['dataset'],
            ui_elements['eval_dataset'],
            ui_elements['format'],
            ui_elements['eval_steps']
        ],
        outputs=[ui_elements['output']]
    )

    ui_elements['stop_button'].click(
        interrupt_training,
        inputs=[],
        outputs=[ui_elements['output']]
    )

    # Refresh dataset and format dropdowns
    def refresh_datasets():
        return gr.update(choices=get_datasets('training/datasets', 'json'))

    def refresh_formats():
        return gr.update(choices=get_datasets('training/formats', 'json'))

    ui_elements['dataset'].change(refresh_datasets, inputs=[], outputs=[ui_elements['dataset']])
    ui_elements['eval_dataset'].change(refresh_datasets, inputs=[], outputs=[ui_elements['eval_dataset']])
    ui_elements['format'].change(refresh_formats, inputs=[], outputs=[ui_elements['format']])