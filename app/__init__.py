from flask import Flask, request, send_from_directory
import os
import json
from dotenv import load_dotenv
from kenzie.image import create_folders, check_file_name, save_file_to_memory, get_files, get_files_by_extensions, download_files

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

    print(file.filename.split('.')[1])

    select_folder = file.filename.split('.')[1]

    if check_file_name(select_folder, file_name):
        return {"status": "conflict", "message": "already have a file with that name"}, 409
    
    save_file_to_memory(select_folder, file)
    
    return {"message": "Upload realizado com sucesso!"}, 201


@app.get('/files')
def get_the_files():
    return get_files(), 200


@app.get('/files/<string:extension>')
def get_the_files_by_extensions(extension):

    items_folder = list()
    
    atual_directory = os.walk(f'./{files_directory}/{extension}')

    if extension not in allowed_extensions:
        return {"status": "error", "message": "not found"}, 404
    
    new_return = get_files_by_extensions(items_folder, atual_directory, extension)

    return new_return, 200
    

@app.get('/download/<string:file_name>')
def download(file_name):
    return download_files(file_name), 200


