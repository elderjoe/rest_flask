import os
from PIL import Image

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'upload')
AUDIO_FOLDER = os.path.join(BASE_DIR, 'audio')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'zip'])

MESSAGE_ROOT = {'message': 'Please upload image or zip file containing images'}
MESSAGE_INVALID = {'message': 'Not a valid file'}
UPLOAD_ROOT = {'message': 'Wrong URL. use /service/uploads/<imagename.ext> or /service/uploads/<foldername>/<imagename.ext>'}

LINK = 'uploads'
FOLDER_NAME = '/upload'

AUDIO_LINK = 'audio'
AUDIO_FOLDER_NAME = '/audio'

YDL_OPTS = {
    'format': 'bestaudio/best',
    'outtmpl': BASE_DIR + '/' + AUDIO_FOLDER_NAME + '/' +'%(title)s.%(ext)s',
    'audioformat': 'mp3',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }],
}

# checks and creates the folder 'upload' if not found
def check_upload_directory():
    if not os.path.exists(BASE_DIR + FOLDER_NAME):
        os.makedirs(BASE_DIR + FOLDER_NAME)

    if not os.path.exists(AUDIO_FOLDER):
        os.makedirs(AUDIO_FOLDER)

def checkImage(uploadfolder, folder, filename):
    try:
        imageDir = '/'.join([uploadfolder, folder, filename])
        Image.open(imageDir)
    except IOError:
        return False
    return True
