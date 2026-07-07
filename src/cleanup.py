from pathlib import Path
def clear_folder(folder):
    folder = Path(folder)
    folder.mkdir(exist_ok=True)
    
    for file in folder.iterdir():
        if file.is_file():
            file.unlink()
    