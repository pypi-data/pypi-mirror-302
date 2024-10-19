from optparse import OptionParser

import confuse
from beets.library import Library
from beets.ui import Subcommand

from .app import create_app
from .server_config import ServerConfig


class ServerCommand(Subcommand):
    _config: ServerConfig

    def __init__(self, config: confuse.Subview):
        self._config = ServerConfig(config)

        parser = OptionParser(usage="%prog")
        parser.add_option(
            '-a', '--address',
            type="string",
            dest="server_address",
            help="address that the server should listen",
            default=self._config.server_address

        )
        parser.add_option(
            '-p', '--port',
            type="int",
            dest="server_port",
            help="port on which the server should listen",
            default=self._config.server_port
        )
        parser.add_option(
            '-d', '--debug',
            action='store_true',
            help="enable Flask debug mode",
            default=self._config.server_debug_mode
        )

        super(ServerCommand, self).__init__(
            parser=parser,
            name="beetmatch-server",
            aliases=["bms"],
            help="Start beetmatch web interface",
        )

    def func(self, lib: Library, options, arguments):
        app = create_app(self._config, lib)
        app.run(host=options.server_address,
                port=options.server_port,
                debug=options.debug)
