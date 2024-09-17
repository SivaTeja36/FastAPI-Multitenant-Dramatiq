from pathlib import Path
import random
import string

def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent

def get_randome_str(chars=string.ascii_letters, N=10):
    return "".join(random.choice(chars) for _ in range(N))