"""A simple HTTP server for transferring files."""

import argparse
from pathlib import Path
from flask import Flask, request, redirect, send_from_directory


app = Flask('__server__')

# download files by making a get to /download/nameOfFile
@app.route('/download/<path:file_name>')
def download_file(file_name):
    """Download the specified file."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], file_name)


# upload files by making a post to /upload
@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload a file to the specified directory."""
    if 'file' not in request.files:
        return redirect('/')

    file = request.files['file']
    if file.filename == '':
        return redirect('/')

    filename = file.filename
    file.save(Path(app.config['UPLOAD_FOLDER'], filename))
    return 'File Uploaded\n'


# list the files in the defined files folder and make them into nice html
def get_files():
    """List the files in the specified directory."""
    html = '<h2>Download</h2>\n'
    dir_root = Path(app.config['UPLOAD_FOLDER'])

    for file in dir_root.rglob('*'):
        if file.is_file():
            file_path = file.relative_to(dir_root)
            html += f'<p><a href=/download/{file_path}>{file_path}</a></p>\n'

    return html


# the root page - graphically upload and download files
@app.route('/', methods=['GET', 'POST'])
def root():
    """Set the content of the root page."""
    return f'''
    <!doctype html>
    <title>Upload new File</title>
    <h2>Upload</h2>
    <form action=/upload method=post enctype=multipart/form-data>
      <input type=file name=file></br></br>
      <input type=submit value=Upload>
    </form>
    </br>
    <h3>Windows</h3>
    <code>certreq -Post -config http://$IP_ADDR:$PORT/upload $FILE</code>
    <h3>Linux</h3>
    <code>curl -X POST -F file=@$FILE http://$IP_ADDR:$PORT/upload</code>
    </br></br>
    {get_files()}
    '''


def arg_parse():
    """Handle command line arguments."""
    parser = argparse.ArgumentParser(
            prog='comment extractor',
            description='extracts comments from html files and webpages')
    parser.add_argument('-f', '--file-dir', default='./files',
            help='directory to use for transfering files')
    parser.add_argument('-p', '--port', default=8000, type=int, help='port number')

    return parser.parse_args()


def main():
    """Main function."""
    args = arg_parse()

    # define the file folder, and create it if it doesn't exist
    file_folder = args.file_dir
    try:
        Path(file_folder).mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        print(f'[!] permissions error while creating file folder: {e}')
        return

    app.config['UPLOAD_FOLDER'] = file_folder
    app.run(host='0.0.0.0', port=args.port)


if __name__ == '__main__':
    main()
