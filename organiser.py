import os
import time
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the path to the downloads folder
downloads_folder = 'C:/Users/smacp/Downloads'

# Define the destination folders for different file types
folders = {
    'Documents': ['.pdf', '.docx', '.txt','.ppt'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif'],
    'Videos': ['.mp4', '.mov', '.avi'],
    'Music': ['.mp3', '.wav', '.aac','.m4a'],
    "Setup":['.exe','.msi','.msu','.rar','.rmskin']
}

# Create destination folders if they don't exist
for folder in folders:
    os.makedirs(os.path.join(downloads_folder, folder), exist_ok=True)
def organize_existing_files():
    # Move existing files to their respective folders
    for filename in os.listdir(downloads_folder):
        source = os.path.join(downloads_folder, filename)

        if os.path.isdir(source):
            # Skip directories
            continue

        # Get the file extension
        _, file_extension = os.path.splitext(filename)
        file_extension = file_extension.lower()
        
        # Check which folder the file belongs to
        moved = False
        for folder, extensions in folders.items():
            if file_extension in extensions:
                destination = os.path.join(downloads_folder, folder, filename)
                shutil.move(source, destination)
                print(f'Moved: {filename} to {folder}')
                moved = True
                break

        if not moved:
            print(f'Skipped: {filename} (unknown file type)')

# Organize existing files before starting observer
organize_existing_files()
class FileHandler(FileSystemEventHandler):
    def on_modified(self,event):
        for filename in os.listdir(downloads_folder):
            source=os.path.join(downloads_folder,filename)
            if os.path.isdir(source):
                continue
            

            _, file_extension=os.path.splitext(filename)
            file_extension=file_extension.lower()
            moved=False
            for folder,extension in folders.items():
                if file_extension in extension:
                    destination=os.path.join(downloads_folder,folder,filename)
                    try:
                        # Try to open the file to ensure it is not being used by another process
                        with open(source, 'rb'):
                            pass
                        
                        # Move the file
                        shutil.move(source, destination)
                        print(f'Moved: {filename} to {folder}')
                        moved = True
                        break
                    except PermissionError:
                        print(f'Skipped: {filename} (file is being used by another process)')
                        moved = True
                        break
                    except Exception as e:
                        print(f'Error moving {filename}: {e}')
                        moved = True
                        break

            if not moved:
                print(f'Skipped: {filename} (unknown file type)')
            if not moved:
                print(f"skipped: {filename}(unknown file type)")
if __name__=="__main__":
    event_handler=FileHandler()
    observer=Observer()
    observer.schedule(event_handler,path=downloads_folder,recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


