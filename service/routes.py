from flask import Blueprint, jsonify, request
import staticVariable
import zipfile
import urllib
import os

UPLOAD_FOLDER = staticVariable.UPLOAD_FOLDER
ALLOWED_EXTENSIONS = staticVariable.ALLOWED_EXTENSIONS
message_root = staticVariable.MESSAGE_ROOT
message_invalid = staticVariable.MESSAGE_INVALID
upload_link = staticVariable.LINK

def add_routes(app=None):
    service = Blueprint('service', __name__)

    def allowed_file(filename):
        return '.' in filename and filename.split('.')[1] in ALLOWED_EXTENSIONS

    def unzip_file(zipname):
        with zipfile.ZipFile(UPLOAD_FOLDER + "/" + zipname.filename, 'r') as z:
            z.extractall(UPLOAD_FOLDER)

    def list_files(UPLOAD_FOLDER, file):
        file_arr = []
        zipName = file.filename.split('.')[0]
        try:
            for fileName in os.listdir(UPLOAD_FOLDER + '/' + zipName):
                if fileName.split('.')[1] in ALLOWED_EXTENSIONS:
                    file_arr.append(fileName)
                else:
                    # deletes all not included in the ALLOWED_EXTENSIONS list
                    os.remove(UPLOAD_FOLDER + '/' + zipName + '/' + fileName)
        except Exception:
            pass

        return file_arr

    def saveImage(req_file):
        fileName = req_file.filename

        if req_file and allowed_file(fileName):
            folder, ext = fileName.split('.')
            if ext == 'zip':
                req_file.save(os.path.join(UPLOAD_FOLDER, fileName))
                unzip_file(req_file)
                files = list_files(UPLOAD_FOLDER, req_file)
                link_arr = []
                base_url = request.base_url

                for dir_file in files:
                    link = '/'.join([base_url, upload_link, folder, dir_file])
                    link_arr.append(link)

                os.remove(UPLOAD_FOLDER + '/' + fileName)
                return jsonify({'links': link_arr})

            else:
                req_file.save(os.path.join(UPLOAD_FOLDER, fileName))
                link = '/'.join([request.base_url, upload_link, fileName])
                return jsonify({'link': link})

        else:
            return jsonify({'response': message_invalid})

    @service.route('/service', methods=['GET','POST'])
    def service_index():
        # checks if the upload directory is available
        staticVariable.check_upload_directory()

        if request.method == 'GET':
            return jsonify({'response': message_root})

        if request.method == 'POST':

            if request.files:
                req_file = request.files['image']
                return saveImage(req_file)
            else:
                image_url = request.args['image']
                imageNewName = request.args['name']

                url_arr = image_url.split('/')
                if allowed_file(url_arr[len(url_arr) - 1]):
                    ext_name = url_arr[len(url_arr) - 1].split('.')[1]

                    imageNewName = '.'.join([imageNewName, ext_name])
                    image_dir = '/'.join([UPLOAD_FOLDER, imageNewName])

                    urllib.urlretrieve(image_url, image_dir)

                    link = '/'.join([request.base_url, upload_link, imageNewName])

                    return jsonify({'link': link})
                else:
                    return jsonify({'response': message_invalid})

    app.register_blueprint(service)
