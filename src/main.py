"""
main.py
Command-line runner for the Music Recommender Simulation.
Runs the recommender for several distinct user profiles so you can compare outputs.
"""

import os
import sys

# Allow running as: python -m src.main  OR  python src/main.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.recommender import load_songs, recommend_songs

# ---------------------------------------------------------------------------
# User profiles (edit these to experiment!)
# ---------------------------------------------------------------------------

PROFILES = {
    "Happy Pop Fan": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "wants_dance": True,
    },
    "Chill Lofi Listener": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.3,
        "wants_dance": False,
    },
    "High-Energy Rock Head": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "wants_dance": False,
    },
    "Sad Indie Night": {
        "genre": "indie",
        "mood": "sad",
        "energy": 0.3,
        "wants_dance": False,
    },
    "EDM Dance Floor": {
        "genre": "edm",
        "mood": "energetic",
        "energy": 0.95,
        "wants_dance": True,
    },
}


# ---------------------------------------------------------------------------
# Pretty-print helpers
# ---------------------------------------------------------------------------

def print_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(f"  🎵  {title}")
    print("=" * 60)


def print_recommendations(recommendations, profile_name: str) -> None:
    print_header(f"Top picks for: {profile_name}")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  {rank}. {song['title']} — {song['artist']}")
        print(f"     Score : {score:.2f}")
        print(f"     Why   : {explanation}")
        print()


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> None:
    # Locate the CSV relative to this file so the script works from any CWD
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "songs.csv")

    songs = load_songs(csv_path)
    print(f"\nLoaded songs: {len(songs)}")

    for profile_name, prefs in PROFILES.items():
        recs = recommend_songs(prefs, songs, k=5)
        print_recommendations(recs, profile_name)


if __name__ == "__main__":
    main()