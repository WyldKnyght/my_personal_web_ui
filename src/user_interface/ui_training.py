# training_ui.py

import gradio as gr
from utils.file_manager import get_available_loras, get_datasets

def create_ui():
    with gr.Tab("Training", elem_id="training-tab"):
        with gr.Row():
            with gr.Column():
                lora_name = gr.Textbox(label='LoRA Name', info='The name of your new LoRA file')
                
                lora_rank = gr.Slider(label='LoRA Rank', value=32, minimum=4, maximum=256, step=4)
                lora_alpha = gr.Slider(label='LoRA Alpha', value=64, minimum=4, maximum=512, step=4)
                
                batch_size = gr.Slider(label='Batch Size', value=128, minimum=1, maximum=256, step=1)
                learning_rate = gr.Textbox(label='Learning Rate', value='3e-4')
                
                epochs = gr.Number(label='Epochs', value=3)
                cutoff_len = gr.Slider(label='Cutoff Length', minimum=32, maximum=2048, value=256, step=32)

            with gr.Column():
                dataset = gr.Dropdown(choices=get_datasets('training/datasets', 'json'), value='None', label='Dataset')
                eval_dataset = gr.Dropdown(choices=get_datasets('training/datasets', 'json'), value='None', label='Evaluation Dataset')
                
                format = gr.Dropdown(choices=get_datasets('training/formats', 'json'), value='None', label='Data Format')
                
                eval_steps = gr.Number(label='Evaluate every n steps', value=100)

        with gr.Row():
            start_button = gr.Button("Start LoRA Training", variant='primary')
            stop_button = gr.Button("Interrupt")

        output = gr.Markdown(value="Ready")

    return {
        'lora_name': lora_name,
        'lora_rank': lora_rank,
        'lora_alpha': lora_alpha,
        'batch_size': batch_size,
        'learning_rate': learning_rate,
        'epochs': epochs,
        'cutoff_len': cutoff_len,
        'dataset': dataset,
        'eval_dataset': eval_dataset,
        'format': format,
        'eval_steps': eval_steps,
        'start_button': start_button,
        'stop_button': stop_button,
        'output': output
    }