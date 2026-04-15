"""
recommender.py
Core logic for the Music Recommender Simulation.
Contains both a functional API (used by main.py) and an OOP API (used by tests).
"""

import csv
from dataclasses import dataclass
from typing import List, Dict, Tuple


# ---------------------------------------------------------------------------
# Data classes (required by tests/test_recommender.py)
# ---------------------------------------------------------------------------

@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


# ---------------------------------------------------------------------------
# OOP Recommender (required by tests/test_recommender.py)
# ---------------------------------------------------------------------------

class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score_song(self, user: UserProfile, song: Song) -> float:
        """Compute a numeric relevance score for a Song given a UserProfile."""
        score = 0.0

        # Genre match: worth the most (2.0 pts)
        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0

        # Mood match: worth 1.5 pts
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.5

        # Energy similarity: max 1.0 pt, linear decay
        energy_gap = abs(song.energy - user.target_energy)
        score += max(0.0, 1.0 - energy_gap)

        # Acoustic preference: +0.5 if user likes acoustic and song is acoustic
        if user.likes_acoustic and song.acousticness >= 0.6:
            score += 0.5
        elif not user.likes_acoustic and song.acousticness < 0.4:
            score += 0.3  # small reward for non-acoustic preference

        return round(score, 4)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k Songs ranked by score for the given UserProfile."""
        scored = [(song, self._score_song(user, song)) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        reasons = []

        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append(f"genre match: {song.genre} (+2.0)")
        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append(f"mood match: {song.mood} (+1.5)")

        energy_gap = abs(song.energy - user.target_energy)
        energy_pts = max(0.0, 1.0 - energy_gap)
        reasons.append(f"energy similarity {song.energy:.1f} vs {user.target_energy:.1f} (+{energy_pts:.2f})")

        if user.likes_acoustic and song.acousticness >= 0.6:
            reasons.append("acoustic match (+0.5)")
        elif not user.likes_acoustic and song.acousticness < 0.4:
            reasons.append("non-acoustic preference (+0.3)")

        return " | ".join(reasons) if reasons else "general match"


# ---------------------------------------------------------------------------
# Functional API (required by src/main.py)
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dictionaries.

    Numerical fields (energy, tempo_bpm, valence, danceability, acousticness)
    are automatically converted to the appropriate Python types.
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Compute a relevance score and explanation for a single song.

    Scoring algorithm:
      +2.0  genre match
      +1.0  mood match
      +0–1  energy similarity  (1.0 minus the absolute gap)
      +0.5  danceability bonus (if user wants dance and song >= 0.7)

    Returns:
        (score, explanation_string)
    """
    score = 0.0
    reasons = []

    # --- Genre match ---
    if song.get("genre", "").lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    # --- Mood match ---
    if song.get("mood", "").lower() == user_prefs.get("mood", "").lower():
        score += 1.0
        reasons.append("mood match (+1.0)")

    # --- Energy similarity ---
    user_energy = float(user_prefs.get("energy", 0.5))
    song_energy = float(song.get("energy", 0.5))
    energy_pts = max(0.0, 1.0 - abs(song_energy - user_energy))
    score += energy_pts
    reasons.append(f"energy similarity (+{energy_pts:.2f})")

    # --- Danceability bonus ---
    if user_prefs.get("wants_dance") and float(song.get("danceability", 0)) >= 0.7:
        score += 0.5
        reasons.append("danceability bonus (+0.5)")

    return round(score, 4), " | ".join(reasons)


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top-k results sorted highest-first.

    Returns:
        List of (song_dict, score, explanation) tuples.
    """
    scored = []
    for song in songs:
        score, explanation = score_song(user_prefs, song)
        scored.append((song, score, explanation))

    # sorted() returns a new list; songs with equal scores keep their CSV order
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]