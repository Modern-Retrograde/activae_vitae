# Здесь запускается Flask.

if __name__ == '__main__':
    from configs import flask_debug
    from main import app as working_app
    from configs import flask_csrf_enabled, flask_secret_key

    working_app.config["CSRF_ENABLED"] = flask_csrf_enabled
    working_app.config["SECRET_KEY"] = flask_secret_key

    working_app.run(debug=flask_debug)
