import os
from flask import Flask, send_file, request
from werkzeug.utils import secure_filename
app = Flask(__name__)
root_dir = os.path.abspath(os.path.dirname(__file__))
hostName = "127.0.0.1"
hostPort = 5000
UPLOAD_FOLDER = root_dir

# Реализация для корневой папки
@app.route('/')
def get_root_list():
    files = os.listdir(root_dir)
    html_code = '<h2><a href="http://' + hostName + ':' + str(hostPort) + '/upload"> Upload to / </a></h2>'
    for el in files:
        if os.path.isfile(root_dir + '/' + el):
            html_code += '<li><a href="http://' + hostName + ':' + str(hostPort) + '/preview/' + el + '">' + el + '</a>'
            html_code += '<a href="http://' + hostName + ':' + str(hostPort) + '/download/' + el + '">' + ' [download]' + '</a>'
            html_code += '<a href="http://' + hostName + ':' + str(hostPort) + '/delete/' + el + '">' + ' [delete]' + '</a>'
            html_code += '</li>'
        else:
            html_code += '<li><a href="http://' + hostName + ':' + str(hostPort) + '/' + el + '">' + el + '/' + '</a>'
            if os.listdir(root_dir + '/' + el) == []:
                html_code += '<a href="http://' + hostName + ':' + str(hostPort) + '/delete/' + el + '">' + ' [del]' + '</a>'
            html_code += '</li>'
    return ('<meta charset="UTF-8"/>' + html_code)

#Реализация для остальных папок
@app.route('/<path:subpath>')
def get_list(subpath):
	directory = root_dir + '/' + subpath
	files = os.listdir(directory)
	html_code = '<h2><a href="http://' + hostName + ':' + str(hostPort) + '/upload/' + subpath + '"> Upload to /' + subpath + '</a></h2>'
	for el in files:
		if os.path.isfile(root_dir + '/' + subpath + '/' + el):
			html_code += '<li><a href="http://' + hostName + ':' + str(hostPort) + '/preview/' + subpath + '/' + el + '">' + el + '</a>'
			html_code += '<a href="http://' + hostName + ':' + str(hostPort) + '/download/' + subpath + '/' + el + '">' + ' [download]' + '</a>'
			html_code += '<a href="http://' + hostName + ':' + str(hostPort) + '/delete/' + subpath + '/' + el + '">' + ' [delete]' + '</a>'
			html_code += '</li>'
		else:
			html_code += '<li><a href="http://' + hostName + ':' + str(hostPort) + '/' + subpath + '/' + el + '">' + el + '/' + '</a>'
			if os.listdir(directory + '/' + el) == []:
				html_code += '<a href="http://' + hostName + ':' + str(hostPort) + '/delete/' + subpath + '/' + el + '">' + ' [del]' + '</a>'
			html_code += '</li>'
	return ('<meta charset="UTF-8"/>' + html_code)



@app.route("/preview/<path:subpath>")
def preview_file(subpath):
    File_dir = root_dir + '/' + subpath
    if not os.path.isfile(File_dir):
        raise Exception("You can't preview directory")
    if os.path.exists(File_dir):
        return send_file(os.path.abspath(File_dir))
    raise Exception("File is not exists")

@app.route("/download/<path:subpath>")
def download_file(subpath):
    File_dir = root_dir + '/' + subpath
    if not os.path.isfile(File_dir):
        raise Exception("You cannot download directory")
    if os.path.exists(File_dir):
        return send_file(os.path.abspath(File_dir), as_attachment=True)
    raise Exception("File not exist")

@app.route("/delete/<path:subpath>")	
def delete(subpath):
    File_dir = root_dir + '/' + subpath
    if not os.path.exists(File_dir):
        raise Exception("Not found")
    if os.path.isfile(File_dir) or os.path.islink(File_dir):
        os.remove(File_dir)
    else:
        os.rmdir(File_dir)
    return "Success"

@app.route("/create_dir/<path:subpath>")
def __create_dir(subpath):
    directory = root_dir + '/' + subpath
    if os.path.exists(directory):
        raise Exception("Folder already exists")
    os.makedirs(directory)
    return "Success"

# корневая папка
@app.route('/upload')
def upload_file_in_root():
	directory = root_dir
	app.config['UPLOAD_FOLDER'] = directory
	return """<html>
   <body>
      <form action = "http://127.0.0.1:5000/uploader" method = "POST" 
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>
   </body>
</html>"""

@app.route('/upload/<path:subpath>')
def upload_file(subpath):
	File_dir = root_dir + '/' + subpath
	app.config['UPLOAD_FOLDER'] = File_dir
	return """<html>
   <body>
      <form action = "http://127.0.0.1:5000/uploader" method = "POST" 
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>
   </body>
</html>"""

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
	if request.method == 'POST':
		f = request.files['file']
		f.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(f.filename)))
		return 'file uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True)
