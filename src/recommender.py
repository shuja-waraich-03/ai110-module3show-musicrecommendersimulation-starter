from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import math

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k Song objects for the given UserProfile (stub — uses functional pipeline)."""
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-English explanation of why this song was recommended to this user (stub)."""
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py

    Reads every row into a dict. Numerical columns are cast to the
    appropriate Python type so math operations work downstream:
      int  : id
      float: energy, tempo_bpm, valence, danceability, acousticness
    All other columns (title, artist, genre, mood) stay as strings.
    """
    import csv

    int_cols   = {"id"}
    float_cols = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for col in int_cols:
                if col in row:
                    row[col] = int(row[col])
            for col in float_cols:
                if col in row:
                    row[col] = float(row[col])
            songs.append(dict(row))

    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

def _gaussian(song_val: float, target: float, sigma: float) -> float:
    """Return a 0–1 similarity using a Gaussian (bell-curve) proximity."""
    return math.exp(-((song_val - target) ** 2) / (2 * sigma ** 2))


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Algorithm recipe
    ----------------
    Categorical bonuses (exact match):
      +2.0  genre matches favorite_genre
      +1.0  mood  matches favorite_mood

    Gaussian proximity for numerical features (weight × similarity):
      energy        weight=3.5, σ=0.25   — strongest vibe signal
      valence       weight=2.5, σ=0.25   — emotional tone
      acousticness  weight=1.5, σ=0.30   — texture preference
      danceability  weight=1.5, σ=0.30   — groove fit
      tempo_bpm     weight=1.0, σ=30.0   — wide tolerance (60–180 BPM range)

    Max possible score: 13.0
    Returns: (score, list_of_reason_strings)
    """
    score = 0.0
    reasons = []

    # --- Categorical bonuses ---
    # +2.0 for an exact genre match — strongest categorical signal
    if song.get("genre") == user_prefs.get("favorite_genre"):
        score += 2.0
        reasons.append(f"genre match '{song['genre']}' (+2.0)")

    # +1.0 for an exact mood match — secondary categorical signal
    if song.get("mood") == user_prefs.get("favorite_mood"):
        score += 1.0
        reasons.append(f"mood match '{song['mood']}' (+1.0)")

    # --- Numerical proximity via Gaussian similarity ---
    # Each feature contributes up to its full weight when song_value == target.
    # The Gaussian ensures a smooth penalty as values diverge, rather than a hard cliff.
    #   contribution = weight × exp( -((song_val - target)² / (2σ²)) )
    #
    # Feature          weight  σ      rationale
    # energy            3.5   0.25   dominant vibe setter
    # valence           2.5   0.25   emotional positivity
    # acousticness      1.5   0.30   texture/tone preference
    # danceability      1.5   0.30   rhythmic groove
    # tempo_bpm         1.0   30.0   wide tolerance for 60–180 BPM range
    numerical = [
        ("energy",       "target_energy",       3.5, 0.25),
        ("valence",      "target_valence",       2.5, 0.25),
        ("acousticness", "target_acousticness",  1.5, 0.30),
        ("danceability", "target_danceability",  1.5, 0.30),
        ("tempo_bpm",    "target_tempo_bpm",     1.0, 30.0),
    ]

    for feature, pref_key, weight, sigma in numerical:
        if pref_key in user_prefs and feature in song:
            sim = _gaussian(float(song[feature]), float(user_prefs[pref_key]), sigma)
            contribution = weight * sim
            score += contribution
            # Only surface a reason when the contribution is meaningful
            if sim >= 0.8:
                reasons.append(
                    f"{feature} very close to target"
                    f" (+{contribution:.2f}/{weight:.1f})"
                )
            elif sim >= 0.5:
                reasons.append(
                    f"{feature} close to target"
                    f" (+{contribution:.2f}/{weight:.1f})"
                )
            else:
                reasons.append(
                    f"{feature} far from target"
                    f" (+{contribution:.2f}/{weight:.1f})"
                )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Steps:
      1. List comprehension scores every song with score_song() in one pass.
      2. sorted() returns a NEW list ranked highest-to-lowest — the original
         order of `songs` is never mutated (unlike .sort() which is in-place).
      3. Slice [:k] takes only the top-k results.

    Each result tuple: (song_dict, score, explanation_string)
    """
    # Score every song in one readable pass
    scored = [
        (song, score, ", ".join(reasons) if reasons else "no strong match")
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    # sorted() leaves `scored` untouched and returns a new ranked list
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
