import gradio as gr
from utils.presets_handler import get_available_presets
from configs import variables

def create_ui():
    with gr.Tab("Parameters", elem_id="parameters-tab"):
        with gr.Row():
            with gr.Column():
                preset_menu = gr.Dropdown(
                    choices=get_available_presets(),
                    value='Default',
                    label='Preset',
                    elem_classes='slim-dropdown'
                )
                save_preset = gr.Button('💾', elem_classes='refresh-button')
                delete_preset = gr.Button('🗑️', elem_classes='refresh-button')

        with gr.Row():
            with gr.Column():
                max_new_tokens = gr.Slider(
                    minimum=1,
                    maximum=2048,
                    step=1,
                    label='Max New Tokens',
                    value=variables.settings['max_new_tokens']
                )
                temperature = gr.Slider(
                    minimum=0.01,
                    maximum=2.0,
                    step=0.01,
                    label='Temperature',
                    value=0.7
                )
                top_p = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    step=0.01,
                    label='Top P',
                    value=0.9
                )
                top_k = gr.Slider(
                    minimum=0,
                    maximum=100,
                    step=1,
                    label='Top K',
                    value=40
                )
                repetition_penalty = gr.Slider(
                    minimum=1.0,
                    maximum=2.0,
                    step=0.01,
                    label='Repetition Penalty',
                    value=1.1
                )

            with gr.Column():
                learning_rate = gr.Slider(
                    minimum=1e-6,
                    maximum=1e-2,
                    step=1e-6,
                    label='Learning Rate',
                    value=1e-4
                )
                num_train_epochs = gr.Slider(
                    minimum=1,
                    maximum=10,
                    step=1,
                    label='Number of Training Epochs',
                    value=3
                )
                batch_size = gr.Slider(
                    minimum=1,
                    maximum=32,
                    step=1,
                    label='Batch Size',
                    value=4
                )
                gradient_accumulation_steps = gr.Slider(
                    minimum=1,
                    maximum=8,
                    step=1,
                    label='Gradient Accumulation Steps',
                    value=1
                )
                warmup_steps = gr.Slider(
                    minimum=0,
                    maximum=1000,
                    step=10,
                    label='Warmup Steps',
                    value=100
                )

        with gr.Row():
            with gr.Column():
                use_8bit_adam = gr.Checkbox(
                    label='Use 8-bit Adam',
                    value=False
                )
                use_peft = gr.Checkbox(
                    label='Use PEFT (Parameter-Efficient Fine-Tuning)',
                    value=True
                )
                lora_r = gr.Slider(
                    minimum=1,
                    maximum=64,
                    step=1,
                    label='LoRA R',
                    value=8,
                    visible=True
                )
                lora_alpha = gr.Slider(
                    minimum=1,
                    maximum=128,
                    step=1,
                    label='LoRA Alpha',
                    value=32,
                    visible=True
                )

    return {
        'preset_menu': preset_menu,
        'save_preset': save_preset,
        'delete_preset': delete_preset,
        'max_new_tokens': max_new_tokens,
        'temperature': temperature,
        'top_p': top_p,
        'top_k': top_k,
        'repetition_penalty': repetition_penalty,
        'learning_rate': learning_rate,
        'num_train_epochs': num_train_epochs,
        'batch_size': batch_size,
        'gradient_accumulation_steps': gradient_accumulation_steps,
        'warmup_steps': warmup_steps,
        'use_8bit_adam': use_8bit_adam,
        'use_peft': use_peft,
        'lora_r': lora_r,
        'lora_alpha': lora_alpha
    }