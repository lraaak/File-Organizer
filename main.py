from pathlib import Path
import shutil
import sys


# chatgpt generated dictionary to organize downloads folder
# modified to work with my gr-10 folder
CAT_TO_EXT = {
    "PDFs": [".pdf"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"],
    "Documents": [".doc", ".docx", ".txt", ".rtf", ".odt", ".tex"],
    "Spreadsheets": [".xls", ".xlsx", ".ods", ".csv"],
    "Presentations": [".ppt", ".pptx", ".odp"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Code": [".py", ".java", ".c", ".cpp", ".js", ".html", ".css", ".php", ".rb", ".go", ".ts"],
    "Executables": [".exe", ".msi", ".apk", ".bat", ".sh"],
    "Design": [".psd", ".ai", ".xd", ".fig", ".sketch"]
}
 

# reversed the array since looping through the initial categories takes n^2 time
ext_to_category = {}
for cat, ext in CAT_TO_EXT.items():
    # extension to category mapping for quick lookup
    for e in ext:
        ext_to_category[e] = cat
        
CATEGORY_NAMES = {f"Sorted {cat}" for cat in CAT_TO_EXT.keys()} | {"Others"}
        

def user_input_path():
    
    while True:
        user_input = input("Enter the full path to your target folder (Type 'EXIT' to close the program): ").strip()
        if user_input.upper() == "EXIT":
            print("Exiting the program.")
            sys.exit(0)
        if not user_input:
            print("Input cannot be empty. Please try again.")
            continue
        
        try:
            target_folder = Path(user_input).expanduser().resolve(strict=True) 
            
            if not target_folder.is_dir():
                print("The specified path exists but is not a directory or folder.")
            else:
                return target_folder
        
        except FileNotFoundError:
            print("The specified path does not exist. Please try again.")
    

def ensure_utf8_printing():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace") # pyright: ignore[reportAttributeAccessIssue]
    except Exception:
        pass

def create_folders(target_folder: Path):
    for cat in CAT_TO_EXT.keys():
        folder_path = target_folder / f"Sorted {cat}"
        folder_path.mkdir(parents=True, exist_ok=True)
        
    other_folder_path = target_folder / "Others"
    other_folder_path.mkdir(parents=True, exist_ok=True)
    
def already_moved(dest_path: Path, root_folder: Path) -> bool:
    try:
        rel_path = dest_path.relative_to(root_folder)
    except ValueError:
        return False
    
    if rel_path.parts[0] in CATEGORY_NAMES and len(rel_path.parts) >= 1:
        return True
    return False
        
                

def organize_downloads(target_folder: Path):
    
    ensure_utf8_printing()
    
    if not target_folder.exists() or not target_folder.is_dir():
        print("The specified directory does not exist or is not a directory.")
        return
    
    for f in target_folder.rglob("*"):
        
        if already_moved(f, target_folder):
            continue
        
        if f.is_file():
            ext = f.suffix.lower()
            cat = ext_to_category.get(ext, "Others")

            if cat == "Others":
                dest_folder = target_folder / "Others"
            else:
                dest_folder = target_folder / f"Sorted {cat}"

            dest_folder.mkdir(exist_ok=True)  # make sure it exists
            dest_path = dest_folder / f.name

            #handle filename conflicts
            counter = 1
            while dest_path.exists():
                new_name = f"{f.stem} ({counter}){f.suffix}"
                dest_path = dest_folder / new_name
                counter += 1

            try:        
                shutil.move(str(f), str(dest_path))
                print(f"Moved: {f.name} -> {dest_path}")
            except Exception as e:
                print(f"Error moving file {f.name}: {e}")
                
            
    print("Organization complete.")

if __name__ == "__main__":
    target_folder = user_input_path()
    create_folders(target_folder)
    organize_downloads(target_folder)
                
                
                
                    
        
                
       
        
