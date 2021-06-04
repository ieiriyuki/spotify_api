#!/usr/bin/env python

import json
from typing import List

import pandas as pd
import requests

from auth import get_client_credentials


def main():
    token = get_client_credentials()

    headers = {
        "Authorization": "{} {}".format(token["token_type"], token["access_token"])
    }

    # Get All New Releases
    get_new_releases(headers=headers)

    # Get Recommendation
    get_recommendation(
        headers=headers,
        seed_artists=["0hSFeqPehe7FtCNWuQ6Bsy"],  # bump of chicken
        seed_genres=["summer", "jazz"],
        seed_tracks=["3hRRYgBeunE3PTmnzATTS0"],  # 天体観測
    )

    return 1


def get_new_releases(headers: dict, country: str = "JP", limit: int = 10):
    """Get a list of new album releases featured in Spotify."""
    url = "https://api.spotify.com/v1/browse/new-releases"

    params = {"country": country, "limit": limit}
    r = requests.get(url, headers=headers, params=params)
    resp = r.json()
    print(json.dumps(resp, indent=2))

    records = []
    for item in resp["albums"]["items"]:
        temp = {
            "album_id": item["id"],
            "album_name": item["name"],
            "type": item["type"],
            "album_type": item["album_type"],
            "artist_1_name": item["artists"][0]["name"],
            "artist_1_id": item["artists"][0]["id"],
        }
        records.append(temp)

    df = pd.DataFrame.from_records(records)
    print(df.head())


def get_recommendation(
    headers: dict,
    seed_artists: List[str],
    seed_genres: List[str],
    seed_tracks: List[str],
    limit: int = 10,
    market: str = "JP",
):
    """Recommendations are generated based on the available information
    for a given seed entity and matched against similar artists and tracks.
    If there is sufficient information about the provided seeds,
    a list of tracks will be returned together with pool size details.
    For artists and tracks that are very new or obscure
    there might not be enough data to generate a list of tracks.

    Available genres are,
    ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime',
     'black-metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat',
     'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical',
     'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal',
     'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub',
     'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french',
     'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove',
     'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle',
     'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm',
     'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance',
     'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino',
     'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno',
     'movies', 'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party',
     'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop',
     'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day',
     'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly',
     'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes',
     'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks',
     'spanish', 'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno',
     'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']
    """
    if len(seed_artists) + len(seed_genres) + len(seed_tracks) > 5:
        raise Exception("seed items are more than 5.")

    url = "https://api.spotify.com/v1/recommendations"
    params = {
        "limit": limit,
        "market": market,
        "seed_artists": ",".join(seed_artists),
        "seed_genres": ",".join(seed_genres),
        "seed_tracks": ",".join(seed_tracks),
    }

    r = requests.get(url, headers=headers, params=params)
    resp = r.json()
    print(json.dumps(resp, indent=2))

    records = []
    for item in resp["tracks"]:
        many_artists = True if len(item["artists"]) > 1 else False
        temp = {
            "id": item["id"],
            "name": item["name"],
            "artist_1_name": item["artists"][0]["name"],
            "artist_1_id": item["artists"][0]["id"],
            "artist_2_name": item["artists"][1]["name"] if many_artists else None,
            "artist_2_id": item["artists"][1]["id"] if many_artists else None,
        }
        records.append(temp)

    df = pd.DataFrame.from_records(records)
    df.to_csv("sample.tsv", sep="\t", index=False)
    print(df.head())

    return 1


if __name__ == "__main__":
    main()
