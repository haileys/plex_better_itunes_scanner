import urllib
import plistlib
import urlparse
import Media
from Utils import Log

Virtual = True


def track_str(track, key):
    if key in track:
        return track[key].encode("utf-8")
    else:
        return None


def Scan(path, files, mediaList, subdirs, language=None, root=None):
    if not root:
        return

    library = plistlib.readPlist(root + "/iTunes Music Library.xml")

    song_kinds = set([
        "AAC audio file",
        "MPEG audio file",
        "Apple Lossless audio file",
        "Matched AAC audio file"
    ])

    path_prefix = urllib.unquote(
        urlparse.urlparse(library["Music Folder"]).path)

    for track in library["Tracks"].values():
        if "Kind" not in track:
            Log("Track {0} has no kind info.".format(track))
            continue
        if not track["Kind"] in song_kinds:
            continue

        plex_track = Media.Track(
            artist=track_str(track, "Artist"),
            album=track_str(track, "Album"),
            title=track_str(track, "Name"),
            album_artist=track_str(track, "Album Artist"),
            index=track.get("Track Number", None),
            disc=track.get("Disc Number", 1),
        )

        if "Location" not in track:
            Log("Track {0} has no location info.".format(track))
            continue
        encoded_path = urlparse.urlparse(track_str(track, "Location")).path

        path = urllib.unquote(encoded_path)

        if not path.startswith(path_prefix):
            Log("Track {0} lives somewhere we can't access".format(track))
            continue

        corrected_path = root + "/iTunes Media/" + path[len(path_prefix):]

        plex_track.parts.append(corrected_path)

        mediaList.append(plex_track)
