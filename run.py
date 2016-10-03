from flask import Flask
import service.routes
import view_upload.routes
import staticVariable
import os

staticVariable.check_upload_directory()

app = Flask(__name__)

service = service.routes
upload = view_upload.routes

service.add_routes(app)
upload.add_routes(app)

if __name__ == '__main__':
    port = in(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
