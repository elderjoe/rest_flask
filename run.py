from flask import Flask
import service.routes
import view_upload.routes
import staticVariable
import os
import site_config as config

staticVariable.check_upload_directory()

app = Flask(__name__)

app.secret_key = config.SECRET_KEY

service = service.routes
upload = view_upload.routes

service.add_routes(app)
upload.add_routes(app)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", config.PORT))
    app.run(debug=True, host=config.HOST, port=port)
