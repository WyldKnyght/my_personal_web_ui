import numpy as np
import torch
import variables, arguments
from transformers import (
    is_torch_npu_available,
    is_torch_xpu_available
)
from ...test.utils.extension_handler import apply_extensions

def encode(prompt, add_special_tokens=True, add_bos_token=True, truncation_length=None):
    if variables.tokenizer is None:
        raise ValueError('No tokenizer is loaded')

    if variables.model.__class__.__name__ in ['LlamaCppModel', 'Exllamav2Model', 'TensorRTLLMModel']:
        input_ids = variables.tokenizer.encode(str(prompt))
        if variables.model.__class__.__name__ not in ['Exllamav2Model']:
            input_ids = np.array(input_ids).reshape(1, len(input_ids))
    else:
        input_ids = variables.tokenizer.encode(str(prompt), return_tensors='pt', add_special_tokens=add_special_tokens)

        if hasattr(variables.tokenizer, 'bos_token_id') and variables.tokenizer.bos_token_id is not None:
            if add_bos_token:
                if (len(input_ids[0]) > 0 and input_ids[0][0] != variables.tokenizer.bos_token_id) or len(input_ids[0]) == 0:
                    # Add a missing bos token (it may not have been added due to faulty model metadata)
                    bos_tensor = torch.tensor([[variables.tokenizer.bos_token_id]])
                    input_ids = torch.cat((bos_tensor, input_ids), 1)

                # Prevent double bos token due to jinja templates with <s> somewhere
                while len(input_ids[0]) > 1 and input_ids[0][0] == variables.tokenizer.bos_token_id and input_ids[0][1] == variables.tokenizer.bos_token_id:
                    input_ids = input_ids[:, 1:]
            else:
                # Remove any bos token that may have been added
                while len(input_ids[0]) > 0 and input_ids[0][0] == variables.tokenizer.bos_token_id:
                    input_ids = input_ids[:, 1:]

    # Handling truncation
    if truncation_length is not None:
        input_ids = input_ids[:, -truncation_length:]

    if variables.model.__class__.__name__ in ['LlamaCppModel', 'Exllamav2Model', 'TensorRTLLMModel'] or arguments.args.cpu:
        return input_ids
    elif arguments.args.deepspeed:
        import deepspeed
        return input_ids.to(deepspeed.get_accelerator().current_device_name())
    elif torch.backends.mps.is_available():
        device = torch.device('mps')
        return input_ids.to(device)
    elif is_torch_xpu_available():
        return input_ids.to("xpu:0")
    elif is_torch_npu_available():
        return input_ids.to("npu:0")
    else:
        return input_ids.cuda()


def decode(output_ids, skip_special_tokens=True):
    if variables.tokenizer is None:
        raise ValueError('No tokenizer is loaded')

    return variables.tokenizer.decode(output_ids, skip_special_tokens=skip_special_tokens)


def get_encoded_length(prompt):
    length_after_extensions = apply_extensions('tokenized_length', prompt)
    if length_after_extensions is not None:
        return length_after_extensions

    return len(encode(prompt)[0])
