from beets.library import Library
from flask import g

from beetsplug.beetmatch.feature.server.server_config import ServerConfig


class BeetsExtension:
    _beets_lib: Library
    _server_config: ServerConfig

    def __init__(self, beets_lib: Library, config: ServerConfig, app=None):
        self._beets_lib = beets_lib
        self._server_config = config

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        def handler():
            g.beets_lib = self._beets_lib
            g.beets_config = self._server_config

        app.before_request(handler)
