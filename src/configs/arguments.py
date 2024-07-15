import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Personal Web UI for Language Models")

    # Model loading arguments
    parser.add_argument('--model', type=str, help='Name of the model to load')
    parser.add_argument('--lora', type=str, help='Name of the LoRA to apply')
    parser.add_argument('--model-dir', type=str, default='models', help='Path to directory containing model files')
    parser.add_argument('--lora-dir', type=str, default='loras', help='Path to directory containing LoRA files')

    # Web UI arguments
    parser.add_argument('--listen', action='store_true', help='Make the web UI available on the network')
    parser.add_argument('--listen-host', type=str, default='0.0.0.0', help='Host to listen on')
    parser.add_argument('--listen-port', type=int, default=7860, help='Port to listen on')
    parser.add_argument('--share', action='store_true', help='Create a public URL')
    parser.add_argument('--auto-launch', action='store_true', help='Open the web UI in the default browser upon launch')

    # Generation arguments
    parser.add_argument('--max-new-tokens', type=int, default=200, help='Maximum number of tokens to generate')
    parser.add_argument('--temperature', type=float, default=0.7, help='Temperature for sampling')
    parser.add_argument('--top-p', type=float, default=0.9, help='Top-p sampling')
    parser.add_argument('--top-k', type=int, default=40, help='Top-k sampling')
    parser.add_argument('--repetition-penalty', type=float, default=1.1, help='Repetition penalty')

    # Model loading options
    parser.add_argument('--cpu', action='store_true', help='Use CPU for inference')
    parser.add_argument('--load-in-8bit', action='store_true', help='Load model in 8-bit mode')
    parser.add_argument('--bf16', action='store_true', help='Use bfloat16 precision')
    parser.add_argument('--no-cache', action='store_true', help='Don\'t use KV cache')

    # Miscellaneous
    parser.add_argument('--verbose', action='store_true', help='Print verbose output')
    parser.add_argument('--seed', type=int, default=-1, help='RNG seed (-1 for random)')

    return parser.parse_args()

# Global variable to hold the parsed arguments
args = parse_arguments()