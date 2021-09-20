from pathlib import Path
from striprtf.striprtf import rtf_to_text

if __name__ == '__main__':
    p = Path.home() /'projects' / 'picky' / 'pickystats' / 'sample.rtf'
    with open(p, 'r') as f:
        text = f.read()
        
