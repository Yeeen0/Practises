import shutil
from pathlib import Path

source_dir = Path('.')
target_dir = Path('./backup')

target_dir.mkdir(exist_ok=True)

for file in source_dir.glob('*.txt'):
    shutil.move(str(file), target_dir / file.name)
    print(f"Moved: {file.name} -> {target_dir}")