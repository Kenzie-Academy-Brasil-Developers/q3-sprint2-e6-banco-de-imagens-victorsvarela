from flask import Flask, request, send_from_directory
import os
import json
from dotenv import load_dotenv
from kenzie.image import create_folders, check_file_name, save_file_to_memory, get_files, get_files_by_extensions, download_files, check_if_exist_folder_with_the_extension_name, check_if_folder_is_empty_the_extension_name, download_zip_files

load_dotenv()

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH'))
files_directory = os.getenv('FILES_DIRECTORY')
allowed_extensions = json.loads(os.getenv('ALLOWED_EXTENSIONS'))

create_folders()

@app.errorhandler(413)
def exceeded_maximum_size(error):
    return {"status": "error", "message": "maximum file size allowed is 1MB"}, 413


@app.post('/upload')
def upload():
    file = request.files['image']

    file_name = file.filename

    select_folder = file_name.split('.')[1]

    if check_file_name(select_folder, file_name):
        return {"status": "conflict", "message": "already have a file with that name"}, 409
    
    save_file_to_memory(select_folder, file)
    
    return {"message": "Upload successful!"}, 201


@app.get('/files')
def get_the_files():
    return get_files(), 200


@app.get('/files/<string:extension>')
def get_the_files_by_extensions(extension):

    if extension not in allowed_extensions:
        return {"status": "error", "message": "not found"}, 404
    
    items_folder = list()
    
    atual_directory = os.walk(f'./{files_directory}/{extension}')
    
    new_return = get_files_by_extensions(items_folder, atual_directory, extension)

    return new_return, 200
    

@app.get('/download/<string:file_name>')
def download(file_name):
    return download_files(file_name), 200


@app.get('/download-zip')
def download_zip():
    name_params = request.args.get('extension')

    if not check_if_exist_folder_with_the_extension_name(name_params):
        return {"status": "error", "message": "not found"}, 404

    if check_if_folder_is_empty_the_extension_name(name_params):
        return {"status": "error", "message": "not found"}, 404

    return download_zip_files(name_params), 200

    