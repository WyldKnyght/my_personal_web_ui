from pathlib import Path

def load_prompt(fname):
    if fname in ['None', '']:
        return ''
    file_path = Path(f'prompts/{fname}.txt')
    if not file_path.exists():
        return ''

    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
        if text[-1] == '\n':
            text = text[:-1]

        return text
