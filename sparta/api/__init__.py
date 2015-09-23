from .base import Base


def blueprint_register(app):
    app.register_blueprint(Base, url_prefix="/base")
    return app
