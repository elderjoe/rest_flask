from flask import Blueprint, jsonify, request
import staticVariable
import zipfile
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

    @service.route('/service', methods=['GET','POST'])
    def service_index():
        # checks if the upload directory is available
        staticVariable.check_upload_directory()

        if request.method == 'GET':
            return jsonify({'response': message_root})

        if request.method == 'POST':
            req_file = request.files['image']
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
                        link_arr.append(base_url
                                        + upload_link
                                        + folder + '/'
                                        + dir_file)

                    os.remove(UPLOAD_FOLDER + '/' + fileName)

                    return jsonify({'links': link_arr})

                else:
                    req_file.save(os.path.join(UPLOAD_FOLDER, fileName))

                    return jsonify({'link': request.base_url
                                            + upload_link
                                            + fileName })

            else:
                return jsonify({'response': message_invalid})


    app.register_blueprint(service)
