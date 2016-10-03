from flask import Blueprint, send_from_directory, jsonify
import staticVariable


def add_routes(app=None):
    upload = Blueprint('upload', __name__)

    @upload.route('/service/uploads/<filename>')
    def single_upload(filename):
        return send_from_directory(staticVariable.UPLOAD_FOLDER, filename)


    @upload.route('/service/uploads/<path>/<filename>')
    def multi_upload(filename, path):
        return send_from_directory(staticVariable.UPLOAD_FOLDER + '/' + path + '/', filename)


    @upload.route('/service/uploads/')
    @upload.route('/service/uploads')
    def root_upload():
        return jsonify({'response': staticVariable.UPLOAD_ROOT})


    @upload.route('/service/audio/<audioname>')
    def audio_upload(audioname):
        return send_from_directory(staticVariable.AUDIO_FOLDER + '/' , audioname)

    app.register_blueprint(upload)
