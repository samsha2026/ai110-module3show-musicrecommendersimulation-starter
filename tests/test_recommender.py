"""
tests/test_recommender.py
Automated tests for the Music Recommender Simulation.
Run with:  pytest
"""

import pytest
from src.recommender import Song, UserProfile, Recommender


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Lo-Fi Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
        Song(
            id=3,
            title="Dark Rock Anthem",
            artist="Rock Band",
            genre="rock",
            mood="intense",
            energy=0.9,
            tempo_bpm=140,
            valence=0.3,
            danceability=0.6,
            acousticness=0.05,
        ),
    ]
    return Recommender(songs)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_recommend_returns_correct_count():
    """recommend() should return exactly k songs."""
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)
    assert len(results) == 2


def test_recommend_returns_songs_sorted_by_score():
    """The pop/happy song should rank first for a pop/happy user."""
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
    rec = make_small_recommender()
    results = rec.recommend(user, k=3)
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_recommend_chill_profile():
    """A chill/lofi user should get the lofi song first."""
    user = UserProfile(favorite_genre="lofi", favorite_mood="chill", target_energy=0.4, likes_acoustic=True)
    rec = make_small_recommender()
    results = rec.recommend(user, k=1)
    assert results[0].genre == "lofi"


def test_explain_recommendation_returns_non_empty_string():
    """explain_recommendation() should return a non-blank string."""
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
    rec = make_small_recommender()
    song = rec.songs[0]
    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_explain_recommendation_mentions_genre_match():
    """Explanation for a matching genre should mention 'genre match'."""
    user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
    rec = make_small_recommender()
    song = rec.songs[0]  # pop song
    explanation = rec.explain_recommendation(user, song)
    assert "genre match" in explanation.lower()


def test_energy_similarity_affects_score():
    """A song with energy closer to the user's target should score higher."""
    user = UserProfile(favorite_genre="other", favorite_mood="other", target_energy=0.8, likes_acoustic=False)
    rec = make_small_recommender()
    # song[0] energy=0.8 (gap 0.0), song[1] energy=0.4 (gap 0.4)
    score_close = rec._score_song(user, rec.songs[0])
    score_far   = rec._score_song(user, rec.songs[1])
    assert score_close > score_far


def test_acoustic_preference_rewards_acoustic_songs():
    """A user who likes acoustic music should see acoustic songs score higher."""
    user_acoustic    = UserProfile(favorite_genre="none", favorite_mood="none", target_energy=0.5, likes_acoustic=True)
    user_nonacoustic = UserProfile(favorite_genre="none", favorite_mood="none", target_energy=0.5, likes_acoustic=False)
    rec = make_small_recommender()
    lofi_song = rec.songs[1]  # acousticness=0.9
    assert rec._score_song(user_acoustic, lofi_song) > rec._score_song(user_nonacoustic, lofi_song)