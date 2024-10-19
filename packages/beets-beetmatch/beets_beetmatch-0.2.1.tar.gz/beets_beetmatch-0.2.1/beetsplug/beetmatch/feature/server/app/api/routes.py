import itertools
import os.path

import flask
from beets.library import Library, Item
from beets.util import py3_path
from flask import url_for
from werkzeug.exceptions import NotFound

from beetsplug.beetmatch.common import pick_random_item
from beetsplug.beetmatch.feature.playlist import PlaylistGenerator
from .blueprint import bp
from ...server_config import ServerConfig


@bp.route('/')
def index():
    return "API Home"


@bp.get("/albums/<int:album_id>/artwork")
def get_album_artwork(album_id: int):
    album = flask.g.beets_lib.get_album(album_id)
    if not album or not album.artpath:
        print(f"artwork: ${album.artpath}")
        return flask.send_from_directory("static", "images/missing-artwork.png")

    return flask.send_file(album.artpath.decode())


@bp.get("/tracks/<int:track_id>/audio")
def get_track_audio(track_id: int):
    track = flask.g.beets_lib.get_item(track_id)
    if not track:
        return flask.abort(404)

    audio_file = py3_path(track.path)
    return flask.send_file(audio_file,
                           as_attachment=True,
                           download_name=os.path.basename(audio_file),
                           conditional=True)


@bp.get("/jukeboxes")
def list_jukeboxes():
    config: ServerConfig = flask.g.beets_config

    return {"jukeboxes": config.jukebox_config.jukeboxes}


@bp.get("/jukeboxes/<jukebox_name>/tracks")
def list_jukebox_tracks(jukebox_name: str):
    config: ServerConfig = flask.g.beets_config
    library: Library = flask.g.beets_lib

    jukebox = config.jukebox_config.get_jukebox(jukebox_name)
    if not jukebox:
        raise NotFound(f"the jukebox '{jukebox_name}' could not be found")

    filter_query = flask.request.args.get("query")
    track_query = jukebox.get_query(additional_query=filter_query)
    offset = flask.request.args.get("offset", default=0, type=int)
    limit = min(flask.request.args.get("limit", default=10, type=int), 100)

    tracks = [track_to_dict(track) for track in itertools.islice(library.items(query=track_query), offset, limit)]

    return {"tracks": tracks}


@bp.post("/playlists")
def create_playlist():
    jukebox_name = flask.request.form["jukeboxName"]
    track_id = flask.request.form.get("seedTrackId", None)
    playlist_length = flask.request.form.get("playlistLength", 10, type=int)

    config: ServerConfig = flask.g.beets_config
    jukebox = config.jukebox_config.get_jukebox(jukebox_name)
    if not jukebox:
        raise NotFound("no jukebox with this name found")

    library: Library = flask.g.beets_lib
    if not track_id:
        tracks = list(library.items(jukebox.get_query()))
        seed_track, _index = pick_random_item(tracks)
        tracks.pop(_index)
    else:
        seed_track = library.get_item(track_id)
        if not seed_track:
            raise NotFound("no track with this id found")
        tracks = list(library.items(jukebox.get_query(f"^id={track_id}")))

    generator = PlaylistGenerator(
        jukebox=jukebox,
        config=config.playlist_config,
        items=tracks,
        seed_item=seed_track
    )

    playlist = [seed_track]
    for track, _ in generator:
        playlist.append(track)
        if len(playlist) >= playlist_length:
            break

    return {"playlist": [track_to_dict(track) for track in playlist]}


def track_to_dict(track: Item):
    return {
        "album": track.get("album"),
        "album_art": url_for("api.get_album_artwork", album_id=track["album_id"]) if track.get("album_id") else None,
        "artist": track["artist"],
        "audio_data": url_for("api.get_track_audio", track_id=track["id"]),
        "bpm": track["bpm"],
        "duration": round(track.length, 3),
        "genre": track["genre"].split(", ") if track.get("genre") else [],
        "id": track["id"],
        "key": f"{track.get('key')} {track.get('key_scale')}" if track.get("key") else None,
        "loudness": round(float(track["average_loudness"]), 3) if track.get("average_loudness") else 1.0,
        "style": track["style"].split(", ") if track.get("style") else [],
        "title": track["title"],
        "year": track["year"],
    }
