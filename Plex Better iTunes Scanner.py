import urllib, plistlib, urlparse, Media

Virtual = True

def track_str(track, key):
  if key in track:
    return track[key].encode("utf-8")
  else:
    return None

def Scan(path, files, mediaList, subdirs, language=None, root=None):
  with open("/Users/charlie/better-itunes.log", "w") as log:
    if not root:
      return

    library = plistlib.readPlist(root + "/iTunes Music Library.xml")

    song_kinds = set([
      "AAC audio file",
      "MPEG audio file",
      "Apple Lossless audio file",
    ])

    path_prefix = urllib.unquote(urlparse.urlparse(library["Music Folder"]).path)

    for track in library["Tracks"].values():
      if not track["Kind"] in song_kinds:
        continue

      plex_track = Media.Track(
        artist       = track_str(track, "Artist"),
        album        = track_str(track, "Album"),
        title        = track_str(track, "Name"),
        album_artist = track_str(track, "Album Artist"),
        index        = track.get("Track Number", None),
        disc         = track.get("Disc Number", 1),
      )

      encoded_path = urlparse.urlparse(track_str(track, "Location")).path

      path = urllib.unquote(encoded_path)

      if not path.startswith(path_prefix):
        # weird, this music file must live somewhere else so we can't access it
        continue

      corrected_path = root + "/iTunes Media/" + path[len(path_prefix):]

      plex_track.parts.append(corrected_path)

      mediaList.append(plex_track)
