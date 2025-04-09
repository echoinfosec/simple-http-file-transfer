import glob, os, sys
from flask import Flask, request, redirect, send_from_directory
from pathlib import Path

app = Flask(__name__)


# define the file folder, and create it if it doesn't exist
FILE_FOLDER = './files'
try:
    Path(FILE_FOLDER).mkdir(parents=True, exist_ok=True)
except Exception as e:
    print('exception while creating file folder:', format(e))
    sys.exit()

app.config['UPLOAD_FOLDER'] = FILE_FOLDER


# download files by making a get to /download/nameOfFile
@app.route('/download/<path:fileName>')
def downloadFile(fileName):
    return send_from_directory(app.config['UPLOAD_FOLDER'], fileName)


# upload files by making a post to /upload 
@app.route('/upload', methods=['POST'])
def uploadFile():
    if 'file' not in request.files:
        return redirect('/')
    
    file = request.files['file']
    if file.filename == '':
        return redirect('/')

    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return 'File Uploaded\n'


# list the files in the defined files folder and make them into nice html
def getFiles():
    html = '<h3>Download</h3>\n'
    root = app.config['UPLOAD_FOLDER']
    lenRoot = len(root)

    files = glob.glob(root + '/**/*', recursive=True)
    for file in files:
        if os.path.isfile(file):
            filePath = file[lenRoot + 1:]
            html += '<p><a href=/download/{}>{}</a></p>\n'.format(filePath, filePath)

    return html

# the root page - graphically upload and download files
@app.route('/', methods=['GET', 'POST'])
def root():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h3>Upload</h1>
    <form action=/upload method=post enctype=multipart/form-data>
      <input type=file name=file></br></br>
      <input type=submit value=Upload>
    </form></br></br>
    ''' + getFiles()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



