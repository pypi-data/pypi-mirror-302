import argparse
import subprocess
import traceback
from typing import Dict, List
from urllib.parse import urlparse

import psutil
import requests


def get_stations(query: str) -> List[Dict]:
    url = "https://radio.garden/api/search"
    params = {"q": query}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    filtered_stations = [
        station
        for station in data["hits"]["hits"]
        if station["_source"]["type"] == "channel" and station["_score"] > 150
    ]

    return [
        {
            "title": station["_source"]["title"],
            "subtitle": station["_source"]["subtitle"],
            "stream": station["_source"]["stream"],
            "score": station["_score"],
        }
        for station in filtered_stations
    ]


def search_stations(query: str):
    try:
        stations = get_stations(query)
        if stations:
            print(f"Found {len(stations)} stations:")
            for station in stations:
                print(
                    f"- {station['title']} - {station['subtitle']} "
                    f"({station['stream']})"
                )
        else:
            print("No stations found matching the query.")
    except requests.RequestException as e:
        print(f"Error searching for stations: {e}")


def play_station(station: str):
    print(f"Attempting to play: {station}")

    # Stop any currently playing station
    stop_playback()

    # Simple URL validation
    parsed_url = urlparse(station)
    if parsed_url.scheme and parsed_url.netloc:
        url_to_play = station
    else:
        # If not a URL, use it as a search query
        try:
            stations = get_stations(station)
            if stations:
                # Sort stations by score in descending order and get the
                # highest scoring one
                highest_scoring_station = max(
                    stations,
                    key=lambda x: x["score"],
                )
                url_to_play = highest_scoring_station["stream"]
                print(
                    f"Playing highest scoring station: "
                    f"{highest_scoring_station['title']}"
                )
            else:
                print("No stations found matching the query.")
                return
        except requests.RequestException as e:
            print(f"Error searching for stations: {e}")
            return

    try:
        # Run mpv command as a background process that continues after the
        # script exits
        subprocess.Popen(
            f"nohup sh -c 'mpv {url_to_play}' > /dev/null 2>&1 &",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"Started playback of {url_to_play}")
    except subprocess.SubprocessError as e:
        print(f"Error starting playback: {e}")


def stop_playback():
    print("Stopping playback")
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == "mpv":
            proc.terminate()
            print("Stopped mpv process")
    print("Playback stopped")


def main():
    parser = argparse.ArgumentParser(description="Beepy Web Radio CLI")
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
    )

    search_parser = subparsers.add_parser("search", help="Search for stations")
    search_parser.add_argument(
        "query", nargs="+", help="Search query (can be multiple words)"
    )

    play_parser = subparsers.add_parser("play", help="Play a station")
    play_parser.add_argument("station", nargs="+", help="Station URL to play")

    subparsers.add_parser("stop", help="Stop playback")

    args = parser.parse_args()

    try:
        if args.command == "search":
            query = " ".join(args.query)
            search_stations(query)
        elif args.command == "play":
            station = " ".join(args.station)
            play_station(station)
        elif args.command == "stop":
            stop_playback()
        else:
            parser.print_help()
    except Exception as e:
        print(f"An error occurred: {e}")
        print("\nDetailed exception information:")
        traceback.print_exc()


if __name__ == "__main__":
    main()
