#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import json
from flask import Flask, jsonify, send_file, flash, request, redirect, url_for, Response
from werkzeug.utils import secure_filename

app = Flask(__name__)
#SANDBOX_PATH = sys.argv[1]
app.config["SANDBOX_PATH"] = "pika"
app.config['UPLOAD_FOLDER'] = app.config["SANDBOX_PATH"]
ALLOWED_EXTENSIONS = frozenset(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


class Sandbox:
    def __init__(self, path):
        self.path = os.path.realpath(path)
    
    def is_in_sandbox(self, path):
        return os.path.commonprefix([self.path, os.path.realpath(path)]) == self.path

class DirectoryTree:
    def __init__(self, path , max_depth = 5, sandbox_path = None):
        if sandbox_path:
            self.sandbox = Sandbox(sandbox_path)
            if not self.sandbox.is_in_sandbox(path):
                raise InvalidUsage('Out of sandbox', status_code=400)
        else:
            self.sandbox = None
        self.max_depth = max_depth
        self.directory_tree = {"back": self.__get_up_path(path, 1),
                               "path": os.path.normpath(path),
                               "name": self.__get_file_name(path),
                               "type": "directory" if self.__is_directory(path) else "file",
                               "size": str(self.__get_size_in_megabytes(path)) + " Mb"
                              }
        if self.max_depth <= 0:
            self.add_meta_data("children" , None)
            return
        if self.__is_directory(path):
            self.add_meta_data("children", self.__scan_children(path))
       
    def __scan_children(self, path):
        if self.sandbox:
            return [DirectoryTree(os.path.join(path, ch), self.max_depth - 1, self.sandbox.path) for ch in os.listdir(path)]
        else:
            return [DirectoryTree(os.path.join(path, ch), self.max_depth - 1) for ch in os.listdir(path)]

    def __get_up_path(self, path, count):
        return os.sep.join(path.split(os.sep)[:-count])

    def add_meta_data(self, name, data):
        self.directory_tree[name] = data
          
    def __str__(self):
        return str(self.directory_tree)
        
    def __get_file_name(self, path):
        return os.path.basename(path)
    
    def __is_directory(self, path):
        return os.path.isdir(path)
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__["directory_tree"], indent=4)
    
    def __get_size_in_megabytes(self, path):
        return round(os.path.getsize(path)/ 2**10 / 2**10, 2)

class InvalidUsage(Exception):
    status_code = 400
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

class FileManager:
    @staticmethod
    def preview_file(path):
        if not os.path.isfile(path):
            raise InvalidUsage("You cannot preview directory", status_code=400)
        if os.path.exists(path):
            return send_file(os.path.abspath(path))
        raise InvalidUsage("File not exist", status_code=400)


    @staticmethod
    def download_file(path):
        if not os.path.isfile(path):
            raise InvalidUsage("You cannot download directory", status_code=400)
        if os.path.exists(path):
            return send_file(os.path.abspath(path), as_attachment=True)
        raise InvalidUsage("File not exist", status_code=400)
    
    @staticmethod
    def upload_file(path, file):
        pass #todo

    @staticmethod
    def delelte_file(path):
        if not os.path.exists(path):
            raise InvalidUsage("Not found", status_code=400)
        os.remove(path)

    @staticmethod
    def create_empty_file(path, data = ""):
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write(data)
        else:
            raise InvalidUsage("File already exist", status_code=400)
            
    @staticmethod
    def create_dir(path):
        if os.path.exists(path):
            raise InvalidUsage("Folder already exists", status_code=400)
        os.makedirs(path)

    @staticmethod
    def delete_empty_dir(path):
        if not os.path.exists(path):
            raise InvalidUsage("Not found", status_code=400)
        os.rmdir(path)


sandbox = Sandbox(app.config["SANDBOX_PATH"])
@app.route("/")
def __index():
    return """
    <head>
    <style>
    .discription {
        font-style: italic;
        font-size: 12px;
    }
    </style>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="script.js"></script>
    </head>
    <body> 
    </body>"""

@app.route("/script.js")
def hoy():
    with open("script.js") as f:
       return Response(f.read(), mimetype="text/javascript")

@app.route("/getJsonOfDir/<path:subpath>")
def __get_json(subpath):
    if not sandbox.is_in_sandbox(subpath):
        raise InvalidUsage('Out of sandbox', status_code=400)
    # return Response(DirectoryTree(subpath,sandbox_path=app.config["SANDBOX_PATH"]).to_json(), mimetype="application/json")
    return DirectoryTree(subpath, sandbox_path=app.config["SANDBOX_PATH"]).to_json()

@app.route("/createDir/<path:subpath>")
def __create_dir(subpath):
    if not sandbox.is_in_sandbox(subpath):
        raise InvalidUsage('Out of sandbox', status_code=400)
    FileManager.create_dir(subpath)
    return DirectoryTree(subpath).to_json()
    
@app.route("/createEmptyFile/<path:subpath>")
def __create_empty_file(subpath):
    if not sandbox.is_in_sandbox(subpath):
        raise InvalidUsage('Out of sandbox', status_code=400)
    FileManager.create_empty_file(subpath)
    return DirectoryTree(subpath).to_json()

@app.route("/delete/<path:subpath>")
def __delete(subpath):
    if not sandbox.is_in_sandbox(subpath):
        raise InvalidUsage('Out of sandbox', status_code=400)
    if os.path.isfile(subpath) or os.path.islink(subpath):
        FileManager.delelte_file(subpath)
    else:
        FileManager.delete_empty_dir(subpath)
    return "Success"

@app.route("/downloadFile/<path:subpath>")
def __download_file(subpath):
    if not sandbox.is_in_sandbox(subpath):
        raise InvalidUsage('Out of sandbox', status_code=400)
    return FileManager.download_file(subpath)

@app.route("/previewFile/<path:subpath>")
def __preview_file(subpath):
    if not sandbox.is_in_sandbox(subpath):
        raise InvalidUsage('Out of sandbox', status_code=400)
    return FileManager.preview_file(subpath)

@app.route('/upload/<path:subpath>')
def upload_file(subpath):
    if not sandbox.is_in_sandbox(subpath):
        raise InvalidUsage('Out of sandbox', status_code=400)
    app.config['UPLOAD_FOLDER'] = subpath
    return """<html>
   <body>
      <form action = "http://localhost:8080/uploader" method = "POST" 
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>
   </body>
</html>"""

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_filee():
    def allowed_file(filename):
        return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    if request.method == 'POST':
        f = request.files['file']
        if not allowed_file(f.filename):
            raise InvalidUsage("Bad file name")
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f.filename)))
        return 'file uploaded successfully'

#StartServer
app.run(debug=True, host="0.0.0.0", port=8080)