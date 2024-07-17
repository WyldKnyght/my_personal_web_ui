# src\model_handlers\llamacpp_model.py
import re
from functools import partial

import numpy as np
import torch

from .handlers.callbacks import Iteratorize
from .loaders.llama_cpp_python_hijack import llama_cpp_lib
from utils.logging_colors import logger
from .handlers.get_max_prompt_length import get_max_prompt_length
from config import model_parameters, ui_settings

def ban_eos_logits_processor(eos_token, input_ids, logits):
    logits[eos_token] = -float('inf')
    return logits


def custom_token_ban_logits_processor(token_ids, input_ids, logits):
    for token_id in token_ids:
        logits[token_id] = -float('inf')

    return logits


class LlamaCppModel:
    def __init__(self):
        self.initialized = False
        self.grammar_string = ''
        self.grammar = None
        self.model = None

    def __del__(self):
        try:
            if hasattr(self, 'model') and self.model is not None:
                if hasattr(self.model, 'close'):
                    self.model.close()
                elif hasattr(self.model, '__del__'):
                    self.model.__del__()
        except Exception as e:
            print(f"Error during model cleanup: {str(e)}")

    @classmethod
    def from_pretrained(cls, path):
        llama_cpp = llama_cpp_lib()
        Llama = llama_cpp.Llama
        LlamaCache = llama_cpp.LlamaCache

        result = cls()
        cache_capacity = 0
        cache_capacity_setting = model_parameters.get_setting('cache_capacity')
        if cache_capacity_setting is not None:
            if 'GiB' in cache_capacity_setting:
                cache_capacity = int(re.sub('[a-zA-Z]', '', cache_capacity_setting)) * 1000 * 1000 * 1000
            elif 'MiB' in cache_capacity_setting:
                cache_capacity = int(re.sub('[a-zA-Z]', '', cache_capacity_setting)) * 1000 * 1000
            else:
                cache_capacity = int(cache_capacity_setting)

        if cache_capacity > 0:
            logger.info(f"Cache capacity is {cache_capacity} bytes")

        tensor_split = model_parameters.get_setting('tensor_split', '').strip()
        tensor_split_list = [float(x) for x in tensor_split.split(",")] if tensor_split else None

        params = {
            'model_path': str(path),
            'n_ctx': model_parameters.get_setting('n_ctx', 2048),
            'n_threads': model_parameters.get_setting('n_threads') or None,
            'n_threads_batch': model_parameters.get_setting('n_threads_batch') or None,
            'n_batch': model_parameters.get_setting('n_batch', 512),
            'use_mmap': model_parameters.get_setting('use_mmap', False),
            'use_mlock': model_parameters.get_setting('mlock', False),
            'mul_mat_q': model_parameters.get_setting('mul_mat_q', True),
            'numa': model_parameters.get_setting('numa', False),
            'n_gpu_layers': model_parameters.get_setting('n_gpu_layers', 0),
            'rope_freq_base': model_parameters.get_setting('rope_freq_base', 10000),
            'tensor_split': tensor_split_list,
            'rope_freq_scale': 1.0 / model_parameters.get_setting('compress_pos_emb', 1.0),
            'offload_kqv': not model_parameters.get_setting('no_offload_kqv', False),
            'split_mode': 2 if model_parameters.get_setting('row_split', False) else 1,
            'flash_attn': model_parameters.get_setting('flash_attn', False)
        }

        logger.info(f"Initializing model with parameters: {params}")

        if model_parameters.get_setting('cache_4bit', False):
            params["type_k"] = 2
            params["type_v"] = 2
        elif model_parameters.get_setting('cache_8bit', False):
            params["type_k"] = 8
            params["type_v"] = 8

        try:
            result.model = Llama(**params)
            if cache_capacity > 0:
                result.model.set_cache(LlamaCache(capacity_bytes=cache_capacity))

            result.initialized = True
            return result, result
        except Exception as e:
            logger.error(f"Error initializing model: {str(e)}")
            raise
    def encode(self, string):
        if type(string) is str:
            string = string.encode()

        return self.model.tokenize(string)

    def decode(self, ids, **kwargs):
        return self.model.detokenize(ids).decode('utf-8')

    def get_logits(self, tokens):
        self.model.reset()
        self.model.eval(tokens)
        logits = self.model._scores
        logits = np.expand_dims(logits, 0)  # batch dim is expected
        return torch.tensor(logits, dtype=torch.float32)

    def load_grammar(self, string):
        if string != self.grammar_string:
            self.grammar_string = string
            if string.strip() != '':
                self.grammar = llama_cpp_lib().LlamaGrammar.from_string(string)
            else:
                self.grammar = None

    def generate(self, prompt, state, callback=None):
        LogitsProcessorList = llama_cpp_lib().LogitsProcessorList
        prompt = prompt if type(prompt) is str else prompt.decode()

        # Handle truncation
        prompt = self.encode(prompt)
        prompt = prompt[-get_max_prompt_length(state):]
        prompt = self.decode(prompt)

        self.load_grammar(state['grammar_string'])
        logit_processors = LogitsProcessorList()
        if state['ban_eos_token']:
            logit_processors.append(partial(ban_eos_logits_processor, self.model.token_eos()))

        if state['custom_token_bans']:
            if to_ban := [int(x) for x in state['custom_token_bans'].split(',')]:
                logit_processors.append(partial(custom_token_ban_logits_processor, to_ban))

        completion_chunks = self.model.create_completion(
            prompt=prompt,
            max_tokens=state['max_new_tokens'],
            temperature=state['temperature'],
            top_p=state['top_p'],
            min_p=state['min_p'],
            typical_p=state['typical_p'],
            frequency_penalty=state['frequency_penalty'],
            presence_penalty=state['presence_penalty'],
            repeat_penalty=state['repetition_penalty'],
            top_k=state['top_k'],
            stream=True,
            seed=int(state['seed']) if state['seed'] != -1 else None,
            tfs_z=state['tfs'],
            mirostat_mode=int(state['mirostat_mode']),
            mirostat_tau=state['mirostat_tau'],
            mirostat_eta=state['mirostat_eta'],
            logits_processor=logit_processors,
            grammar=self.grammar
        )

        output = ""
        for completion_chunk in completion_chunks:
            if ui_settings.stop_everything:
                break

            text = completion_chunk['choices'][0]['text']
            output += text
            if callback:
                callback(text)

        return output

    def generate_with_streaming(self, *args, **kwargs):
        with Iteratorize(self.generate, args, kwargs, callback=None) as generator:
            reply = ''
            for token in generator:
                reply += token
                yield reply
