from flask import Flask
application = Flask(__name__)

if __name__ == "__main__":
    application.config.from_object('config')
    application.run(host='0.0.0.0')

from app import views
