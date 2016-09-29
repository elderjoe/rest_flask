import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'upload')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'zip'])

MESSAGE_ROOT = {'message': 'Please upload image or zip file containing images'}
MESSAGE_INVALID = {'message': 'Not a valid file'}
UPLOAD_ROOT = {'message': 'Wrong URL. use /service/uploads/<imagename.ext> or /service/uploads/<foldername>/<imagename.ext>'}

LINK = '/uploads/'
FOLDER_NAME = '/upload'

# checks and creates the folder 'upload' if not found
def check_upload_directory():
    if not os.path.exists(BASE_DIR + FOLDER_NAME):
        os.makedirs(BASE_DIR + FOLDER_NAME)
