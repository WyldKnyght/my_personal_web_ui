import os
import json
from pathlib import Path

def get_available_prompts():
    prompts_dir = Path('prompts')
    available_prompts = ['None']

    if prompts_dir.is_dir():
        for file in prompts_dir.iterdir():
            if file.suffix == '.json':
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        prompt_data = json.load(f)
                        if 'name' in prompt_data:
                            available_prompts.append(prompt_data['name'])
                        else:
                            available_prompts.append(file.stem)
                except json.JSONDecodeError:
                    print(f"Error reading {file}. Skipping.")
            elif file.suffix == '.txt':
                available_prompts.append(file.stem)

    return sorted(available_prompts)
