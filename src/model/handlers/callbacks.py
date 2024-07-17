# src/model_handlers/callbacks.py
import gc
import traceback
import torch
import transformers
from transformers import is_torch_npu_available, is_torch_xpu_available
from queue import Queue
from threading import Thread
from config import model_parameters, ui_settings

class StopNowException(Exception):
    """Custom exception to signal the need to stop iteration."""
    pass

class _StopEverythingStoppingCriteria(transformers.StoppingCriteria):
    """Custom stopping criteria that stops when ui_settings.stop_everything is True."""

    def __init__(self):
        super().__init__()

    def __call__(self, input_ids: torch.LongTensor, _scores: torch.FloatTensor) -> bool:
        return ui_settings.stop_everything

class Stream(transformers.StoppingCriteria):
    """Custom stopping criteria that calls a callback function on each step."""

    def __init__(self, callback_func=None):
        super().__init__()
        self.callback_func = callback_func

    def __call__(self, input_ids, scores) -> bool:
        if self.callback_func is not None:
            self.callback_func(input_ids[0])
        return False

class Iteratorize:
    """
    Transforms a function that takes a callback into a lazy iterator (generator).

    Adapted from: https://stackoverflow.com/a/9969000
    """

    def __init__(self, func, args=None, kwargs=None, callback=None):
        self.mfunc = func
        self.c_callback = callback
        self.q = Queue()
        self.sentinel = object()
        self.args = args or []
        self.kwargs = kwargs or {}
        self.stop_now = False

        def _callback(val):
            if self.stop_now or ui_settings.stop_everything:
                raise StopNowException
            self.q.put(val)

        def gentask():
            try:
                ret = self.mfunc(callback=_callback, *self.args, **self.kwargs)
            except StopNowException:
                pass
            except Exception:
                traceback.print_exc()
            clear_torch_cache()
            self.q.put(self.sentinel)
            if self.c_callback:
                self.c_callback(ret)

        self.thread = Thread(target=gentask)
        self.thread.start()

    def __iter__(self):
        return self

    def __next__(self):
        obj = self.q.get(True, None)
        if obj is self.sentinel:
            raise StopIteration
        else:
            return obj

    def __del__(self):
        clear_torch_cache()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_now = True
        clear_torch_cache()

def clear_torch_cache():
    """Clears the PyTorch cache."""
    gc.collect()
    if not model_parameters.get_setting('n_gpu_layers'):
        if is_torch_xpu_available():
            torch.xpu.empty_cache()
        elif is_torch_npu_available():
            torch.npu.empty_cache()
        else:
            torch.cuda.empty_cache()
