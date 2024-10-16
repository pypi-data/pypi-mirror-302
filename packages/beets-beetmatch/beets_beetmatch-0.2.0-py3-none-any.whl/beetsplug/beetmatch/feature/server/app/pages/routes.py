import flask
from flask import request

from .blueprint import bp


@bp.route("/frames/<path>")
def render_frame(path):
    return flask.render_template(f"frames/{path}")


@bp.route("/")
def homepage():
    return flask.render_template("index.html")


@bp.route("/playlist")
def create_playlist():
    return flask.render_template("playlist_create.html")


@bp.route("/playlist/new")
def generate_playlist():
    return flask.render_template("playlist.html",
                                 seedTrackId=request.args.get('seedTrackId'),
                                 jukebox=request.args.get('jukebox'),
                                 playlistSize=request.args.get('playlistSize'))
