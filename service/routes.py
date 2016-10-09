from __future__ import unicode_literals

from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for
import staticVariable
from staticVariable import checkImage
from youtube_dl import YoutubeDL
import zipfile
import urllib
import os

UPLOAD_FOLDER = staticVariable.UPLOAD_FOLDER
ALLOWED_EXTENSIONS = staticVariable.ALLOWED_EXTENSIONS
AUDIO_FOLDER = staticVariable.AUDIO_FOLDER
message_root = staticVariable.MESSAGE_ROOT
message_invalid = staticVariable.MESSAGE_INVALID
upload_link = staticVariable.LINK
audio_link = staticVariable.AUDIO_LINK
ydl_opts = staticVariable.YDL_OPTS

def add_routes(app=None):
    service = Blueprint('service', __name__,
                        template_folder='templates',
                        static_folder='./static',
                        static_url_path='/service/static')

    def allowed_file(filename):
        return '.' in filename and filename.split('.')[1] in ALLOWED_EXTENSIONS

    def unzip_file(zipname):
        zipinfo = zipfile.ZipFile(zipname)
        CREATED_FOLDER = ''
        for z in zipinfo.filelist:
            if not z.filename.endswith('/'):
                folderName = zipname.filename.split('.')[0]
                CREATED_FOLDER = '/'.join([UPLOAD_FOLDER, folderName])
                if not os.path.exists(CREATED_FOLDER):
                    os.makedirs(CREATED_FOLDER)
            else: break

        with zipfile.ZipFile(UPLOAD_FOLDER + "/" + zipname.filename, 'r') as z:
            if CREATED_FOLDER:
                z.extractall(CREATED_FOLDER)
            else: z.extractall(UPLOAD_FOLDER)

    def list_files(UPLOAD_FOLDER, file):
        file_arr = []
        zipName = file.filename.split('.')[0]

        try:
            for fileName in os.listdir(UPLOAD_FOLDER + '/' + zipName):
                if fileName.split('.')[1] in ALLOWED_EXTENSIONS and \
                    checkImage(UPLOAD_FOLDER, zipName, fileName):
                    file_arr.append(fileName)
                else:
                    os.remove(UPLOAD_FOLDER + '/' + zipName + '/' + fileName)

        except Exception:
            pass

        return file_arr

    def saveImage(req_file):
        fileName = req_file.filename

        if req_file and allowed_file(fileName):
            folder, ext = fileName.split('.')
            base_url = request.base_url
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
                link = '/'.join([base_url, upload_link, fileName])
                return jsonify({'link': link})

        else:
            return jsonify({'response': message_invalid})

    def upload_image_from_url(image_url, imageNewName):
        url_arr = image_url.split('/')
        if allowed_file(url_arr[len(url_arr) - 1]):
            ext_name = url_arr[len(url_arr) - 1].split('.')[1]

            imageNewName = '.'.join([imageNewName, ext_name])
            image_dir = '/'.join([UPLOAD_FOLDER, imageNewName])

            urllib.urlretrieve(image_url, image_dir)
            base_url = request.base_url
            link = '/'.join([base_url, upload_link, imageNewName])

            return jsonify({'link': link})
        else:
            return jsonify({'response': message_invalid})

    def upload_video(service, name, url):
        yt_url = url
        ytdl = YoutubeDL()
        
        if name:
            audio_name = '.'.join([name.replace(' ','_'), 'mp3'])
        else:
            info = ytdl.extract_info(yt_url, download=False)
            audio_name = '.'.join([info['title'].replace(' ','_'), 'mp3'])

        ydl_opts['outtmpl'] =  '/'.join([audio_link, audio_name])

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])

        link = '/'.join([request.base_url, ydl_opts['outtmpl']])
        if service == 'API':
            return jsonify({'link': link})
        else:
            return link

    @service.route('/service', methods=['GET','POST'])
    def service_index():

        staticVariable.check_upload_directory()

        if request.method == 'GET':
            return jsonify({'response': message_root})

        if request.method == 'POST':

            if request.files:
                req_file = request.files['file']
                return saveImage(req_file)

            if 'file' in request.args:
                image_url = request.args['file']
                imageNewName = request.args['name']
                return upload_image_from_url(image_url, imageNewName)
            else:
                yt_url = request.args['url']
                API = 'API'
                return upload_video(API, '', yt_url)

            return jsonify({'response': message_invalid})

    @service.route('/', methods=['GET','POST'])
    def service_ui():
        if request.method == 'POST':
            url = request.form['url']
            name = request.form['name']
            if url:
                yt_link = upload_video('FORM', name, url)
                idx = yt_link.find('/audio')
                yt_link = ''.join([yt_link[:idx],'download',yt_link[idx:]])
                session['link'] = yt_link
                return redirect(url_for('service.service_ui'))
            else:
                return render_template('index.html', url='URL not found')
        else:
            return render_template('index.html', url='')

    app.register_blueprint(service)
