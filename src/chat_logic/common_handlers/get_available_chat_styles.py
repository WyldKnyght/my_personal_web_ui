from pathlib import Path
from utils.natural_keys import natural_keys

def get_available_chat_styles():
    return sorted(
        {
            '-'.join(k.stem.split('-')[1:])
            for k in Path('css').glob('chat_style*.css')
        },
        key=natural_keys,
    )

