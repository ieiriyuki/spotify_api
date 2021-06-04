#!/usr/bin/env python

import json
from pathlib import Path
from typing import List

import pandas as pd
import requests

from auth import get_client_credentials


def main():
    token = get_client_credentials()

    headers = {
        "Authorization": "{} {}".format(token["token_type"], token["access_token"])
    }
    artist_id = "0hSFeqPehe7FtCNWuQ6Bsy"  # bump of chickenのid

    # アーティストのトップトラック
    r = get_top_tracks(headers=headers, id=artist_id, market="JP")
    resp = r.json()
    print(json.dumps(resp, indent=2, sort_keys=True))

    df = parse_tracks(resp["tracks"])
    print(df.head())

    df.to_csv(make_data_path("sample_top_tracks.csv"), index=False)

    # アーティストに関連するアーティスト
    r = get_related_artists(headers=headers, id=artist_id)
    resp = r.json()
    print(json.dumps(resp, indent=2, sort_keys=True))

    df = parse_related_artists(resp["artists"])
    print(df.head())

    return 1


def get_top_tracks(headers: dict, id: str, market: str):
    """Get Spotify catalog information about an artist’s top tracks by country."""
    url = f"https://api.spotify.com/v1/artists/{id}/top-tracks"

    params = {"market": market}
    r = requests.get(url, headers=headers, params=params)

    return r


def parse_tracks(items: List[dict]) -> pd.DataFrame:
    """parse track information of json format"""
    records = []
    for item in items:
        album = item["album"]
        temp = {
            "id": item["id"],
            "name": item["name"],
            "popularity": item["popularity"],
            # "external_url": item["external_urls"]["spotify"],  # トラックのページ
            # "preview_url": item["preview_url"],  " 30秒のクリップを聴ける"
            "album_id": album["id"],
            "album_type": album["album_type"],
            # "album_ex_url": album["external_urls"]["spotify"],  # アルバムのページ
            "album_name": album["name"],
            "album_release_date": album["release_date"],
            "album_total_tracks": album["total_tracks"],
        }
        records.append(temp)

    df = pd.DataFrame.from_records(records)

    return df


def get_related_artists(headers: dict, id: str):
    """Get Spotify catalog information about artists similar to a given artist. Similarity is based on analysis of the Spotify community’s listening history."""
    url = f"https://api.spotify.com/v1/artists/{id}/related-artists"
    r = requests.get(url, headers=headers)

    return r


def parse_related_artists(items: List[dict]) -> pd.DataFrame:
    """parse artist information of json format"""
    records = []
    for item in items:
        temp = {
            "id": item["id"],
            "name": item["name"],
            "popularity": item["popularity"],
            "followers_total": item["followers"]["total"],
            # "genres": item["genres"],
            # "external_urls": item["external_urls"]["spotify"]
        }
        records.append(temp)
    return pd.DataFrame.from_records(records)


def make_data_path(file_name: str) -> str:
    """make path to data file"""
    parent = Path(__file__).parent.parent
    data_path = Path.joinpath(parent, "data", file_name).resolve()
    return data_path


if __name__ == "__main__":
    main()
