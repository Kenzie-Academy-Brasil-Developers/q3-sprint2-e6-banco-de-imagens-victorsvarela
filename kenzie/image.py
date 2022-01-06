
from flask import send_from_directory, jsonify
from genericpath import exists
import os
import json
from dotenv import load_dotenv

load_dotenv()

#allowed_extensions = ['jpg', 'png', 'gif']
#allowed_extensions = json.loads(os.environ['ALLOWED_EXTENSIONS'])
allowed_extensions = json.loads(os.getenv('ALLOWED_EXTENSIONS'))

files_directory = os.getenv('FILES_DIRECTORY')

def create_folders():

    if not os.path.exists(f'./{files_directory}'):
        os.system(f'mkdir {files_directory}')

    for dirnames in allowed_extensions:
        if not os.path.exists(f'./{files_directory}/{dirnames}'):
            os.system(f'mkdir ./{files_directory}/{dirnames}')
            print(dirnames)


def check_file_name(select_folder, file_name):
    return os.path.isfile(f'./{files_directory}/{select_folder}/{file_name}')


def save_file_to_memory(select_folder, file):
    file.save(os.path.join(f'./{files_directory}/{select_folder}/', file.filename))


def get_files():
    items_folders = list()

    atual_directory = os.walk(f'./{files_directory}')

    for _, _, filenames in atual_directory:
        items_folders.append(filenames)

    del(items_folders[0])
    
    print(items_folders)

    return jsonify(
        png=items_folders[0],
        gif=items_folders[1],
        jpg=items_folders[2]
    )


def get_files_by_extensions(items_folder, atual_directory, extension):

    for _, _, filenames in atual_directory:
        items_folder.extend(filenames)

    return {
        extension: items_folder
    }


def download_files(file_name):
    print(file_name)
    extension_file = file_name.split('.')[1]

    return send_from_directory(
        directory=f"../{files_directory}/{extension_file}/", 
        path=f"{file_name}", 
        as_attachment=True
    )