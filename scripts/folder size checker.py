import os

os.system("cls" if os.name == "nt" else "clear")

def get_folder_size(folder_path='.'):
    
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
            except: 
                pass
    return total_size

def get_direct_subfolder_sizes(folder_path='.'):
    subfolder_sizes = {}
    for d in os.listdir(folder_path):
        try:
            subdir_path = os.path.join(folder_path, d)
            if os.path.isdir(subdir_path):
                subfolder_sizes[subdir_path] = get_folder_size(subdir_path)
        except: 
            pass
    return subfolder_sizes

def list_direct_subfolder_sizes(folder_path='.'):
    subfolder_sizes = get_direct_subfolder_sizes(folder_path)
    subfolder_sizes = {k: v / (1024 * 1024) for k, v in subfolder_sizes.items()}
    sorted_sizes = sorted(subfolder_sizes.items(), key=lambda x: x[1], reverse=True)
    for subdir, size in sorted_sizes:
        print(f"Folder: {os.path.abspath(subdir)} | Size: {size:.2f} MB")

def get_file_sizes(directory):
    file_sizes = []
    
    for filename in os.listdir(directory):
        try:
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                size_bytes = os.path.getsize(file_path)
                size_mb = size_bytes / (1024 * 1024) 
                file_sizes.append((filename, size_mb))
        except: 
            pass
    
    file_sizes = sorted(file_sizes, key=lambda x: x[1], reverse=True)
    
    return file_sizes

while True:
    try:
        directory = input('Enter the directory path: ')
        if not os.path.isdir(directory):
            print('Invalid directory:')
            continue
        list_direct_subfolder_sizes(directory)
        sizes = get_file_sizes(directory)
        for filename, size_mb in sizes:
            print(f"File: {directory}\{filename} | Size: {size_mb:.2f} MB")
    except Exception as e:
        print(f'An error has occured: {e}')

