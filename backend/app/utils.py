# utils.py
import re

def clean_name_for_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', '', name)
