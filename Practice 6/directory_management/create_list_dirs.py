from pathlib import Path

# Выводит список всех папок в текущей директории
dirs = [d.name for d in Path('.').iterdir() if d.is_dir()]

print("Finds directory:")
print('\n'.join(dirs) if dirs else "No files")