import gradio as gr
from utils.lora_handler import get_available_loras
from utils.get_available_models import get_available_models
from utils.create_refresh_button import create_refresh_button
from configs import arguments, variables

def create_ui():
    with gr.Tab("Model", elem_id="model-tab"):
        with gr.Row():
            with gr.Column():
                with gr.Row():
                    model_menu = gr.Dropdown(
                        choices=get_available_models(),
                        value=lambda: variables.model_name,
                        label='Model',
                        elem_classes='slim-dropdown'
                    )
                    create_refresh_button(
                        model_menu,
                        lambda: None,
                        lambda: {'choices': get_available_models()},
                        'refresh-button'
                    )
                    load_model = gr.Button("Load", visible=not variables.settings['autoload_model'], elem_classes='refresh-button')
                    unload_model = gr.Button("Unload", elem_classes='refresh-button')
                    reload_model = gr.Button("Reload", elem_classes='refresh-button')
                    save_model_settings = gr.Button("Save settings", elem_classes='refresh-button')

                with gr.Row():
                    lora_menu = gr.Dropdown(
                        multiselect=True,
                        choices=get_available_loras(),
                        value=variables.lora_names,
                        label='LoRA(s)',
                        elem_classes='slim-dropdown'
                    )
                    create_refresh_button(
                        lora_menu,
                        lambda: None,
                        lambda: {'choices': get_available_loras(), 'value': variables.lora_names},
                        'refresh-button'
                    )
                    lora_menu_apply = gr.Button(value='Apply LoRAs', elem_classes='refresh-button')

                with gr.Row():
                    loader = gr.Dropdown(
                        label="Model loader",
                        choices=["Transformers", "llama.cpp"],
                        value=None
                    )

                n_ctx = gr.Slider(
                    minimum=0,
                    maximum=variables.settings['truncation_length_max'],
                    step=256,
                    label="Context length (n_ctx)",
                    value=arguments.args.n_ctx,
                    info='Try lowering this if you run out of memory while loading the model.'
                )

                n_gpu_layers = gr.Slider(
                    label="GPU layers",
                    minimum=0,
                    maximum=256,
                    value=arguments.args.n_gpu_layers,
                    info='Number of layers to offload to GPU. Must be > 0 to use GPU.'
                )

                n_batch = gr.Slider(
                    label="Batch size",
                    minimum=1,
                    maximum=2048,
                    step=1,
                    value=arguments.args.n_batch
                )

                threads = gr.Slider(
                    label="CPU threads",
                    minimum=0,
                    step=1,
                    maximum=256,
                    value=arguments.args.threads
                )

                n_gqa = gr.Slider(
                    label="Group Query Attention",
                    minimum=1,
                    maximum=256,
                    step=1,
                    value=arguments.args.n_gqa,
                    info='Grouped Query Attention factor (only for LLaMA-2)'
                )

                rope_freq_base = gr.Slider(
                    label='RoPE frequency base',
                    minimum=0,
                    maximum=1000000,
                    step=1000,
                    value=arguments.args.rope_freq_base,
                    info='If > 0, will be used instead of alpha_value. Related by rope_freq_base = 10000 * alpha_value ^ (64 / 63)'
                )

                rope_freq_scale = gr.Slider(
                    label='RoPE frequency scaling',
                    minimum=0,
                    maximum=2,
                    step=0.01,
                    value=arguments.args.rope_freq_scale,
                    info='Used for context expansion. 1 / compress_pos_emb'
                )

                with gr.Row():
                    use_flash_attention_2 = gr.Checkbox(
                        label="Use Flash Attention 2",
                        value=arguments.args.use_flash_attention_2,
                        info='Faster but uses more VRAM'
                    )

                    cache_8bit = gr.Checkbox(
                        label="8-bit cache",
                        value=arguments.args.cache_8bit,
                        info='Use 8-bit cache to save VRAM'
                    )

                    cpu = gr.Checkbox(
                        label="CPU mode",
                        value=arguments.args.cpu,
                        info='Use CPU only (no GPU acceleration)'
                    )

                    mlock = gr.Checkbox(
                        label="mlock",
                        value=arguments.args.mlock,
                        info='Force system to keep model in RAM'
                    )

                    numa = gr.Checkbox(
                        label="NUMA",
                        value=arguments.args.numa,
                        info='Non-Uniform Memory Access support'
                    )

                    bf16 = gr.Checkbox(
                        label="bfloat16",
                        value=arguments.args.bf16,
                        info='Use bfloat16 precision (Ampere+ GPUs)'
                    )

                autoload_model = gr.Checkbox(
                    value=variables.settings['autoload_model'],
                    label='Autoload the model',
                    info='Load the model as soon as it is selected in the Model dropdown'
                )

    return {
        'model_menu': model_menu,
        'load_model': load_model,
        'unload_model': unload_model,
        'reload_model': reload_model,
        'save_model_settings': save_model_settings,
        'lora_menu': lora_menu,
        'lora_menu_apply': lora_menu_apply,
        'loader': loader,
        'n_ctx': n_ctx,
        'n_gpu_layers': n_gpu_layers,
        'n_batch': n_batch,
        'threads': threads,
        'n_gqa': n_gqa,
        'rope_freq_base': rope_freq_base,
        'rope_freq_scale': rope_freq_scale,
        'use_flash_attention_2': use_flash_attention_2,
        'cache_8bit': cache_8bit,
        'cpu': cpu,
        'mlock': mlock,
        'numa': numa,
        'bf16': bf16,
        'autoload_model': autoload_model
    }