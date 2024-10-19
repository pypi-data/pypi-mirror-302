import jinja_partials
from beets.library import Library
from flask import Flask
from turbo_flask import Turbo

from beetsplug.beetmatch.feature.server.app.extensions import BeetsExtension
from beetsplug.beetmatch.feature.server.server_config import ServerConfig

turbo = Turbo()


def create_app(config: ServerConfig, beets_lib: Library):
    app = Flask(__name__)
    app.config.from_object({
        "TEMPLATES_AUTO_RELOAD": config.server_debug_mode
    })

    turbo.init_app(app)

    jinja_partials.register_extensions(app)

    # Extensions
    beets_ext = BeetsExtension(app=app, beets_lib=beets_lib, config=config)

    # Blueprints
    from .api import bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    from .pages import bp as pages_blueprint
    app.register_blueprint(pages_blueprint)

    return app
