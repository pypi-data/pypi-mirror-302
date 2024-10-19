import confuse

from beetsplug.beetmatch import JukeboxConfig
from beetsplug.beetmatch.feature.playlist import PlaylistConfig

_DEFAULT_CONFIG = {
    "server": {
        "address": "0.0.0.0",
        "port": 8447,
        "cors": "",
        "debug_mode": False
    },
}


class ServerConfig:
    _config: confuse.Subview

    _jukebox: JukeboxConfig
    _playlist: PlaylistConfig

    def __init__(self, config: confuse.Subview):
        self._config = config
        self._config.add(_DEFAULT_CONFIG)

        self._playlist = PlaylistConfig(config)
        self._jukebox = JukeboxConfig(config)

    @property
    def server_address(self):
        return self._config["server"]["address"].as_str()

    @property
    def server_port(self):
        return self._config["server"]["port"].get(int)

    @property
    def server_cors_header(self):
        return self._config["server"]["cors"].as_str()

    @property
    def server_debug_mode(self):
        return self._config["server"]["debug_mode"].get(bool)

    @property
    def playlist_config(self):
        return self._playlist

    @property
    def jukebox_config(self):
        return self._jukebox
