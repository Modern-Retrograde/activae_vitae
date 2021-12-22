# Здесь запускается Flask.

if __name__ == '__main__':
    from configs import flask_debug
    from main import app as working_app

    working_app.run(debug=flask_debug)
