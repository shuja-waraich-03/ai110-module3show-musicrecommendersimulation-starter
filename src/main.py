"""
Command line runner for the Music Recommender Simulation.

Run with:
    python -m src.main        (from project root)
    python src/main.py        (from project root)
"""

try:
    from src.recommender import load_songs, recommend_songs  # python -m src.main
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs      # python src/main.py


# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------

PROFILES = [
    # ------------------------------------------------------------------
    # 1. Standard profiles
    # ------------------------------------------------------------------
    {
        "_name": "High-Energy Pop",
        "_description": "Party mode — loud, fast, danceable pop",
        "favorite_genre":      "pop",
        "favorite_mood":       "happy",
        "target_energy":        0.90,
        "target_valence":       0.85,
        "target_acousticness":  0.05,
        "target_danceability":  0.88,
        "target_tempo_bpm":   128.0,
    },
    {
        "_name": "Chill Lofi",
        "_description": "Late-night focus session — calm, warm, acoustic-ish",
        "favorite_genre":      "lofi",
        "favorite_mood":       "chill",
        "target_energy":        0.40,
        "target_valence":       0.55,
        "target_acousticness":  0.70,
        "target_danceability":  0.60,
        "target_tempo_bpm":    80.0,
    },
    {
        "_name": "Deep Intense Rock",
        "_description": "High-energy, heavy, guitar-driven — workout or commute",
        "favorite_genre":      "rock",
        "favorite_mood":       "intense",
        "target_energy":        0.92,
        "target_valence":       0.40,
        "target_acousticness":  0.08,
        "target_danceability":  0.65,
        "target_tempo_bpm":   150.0,
    },

    # ------------------------------------------------------------------
    # 2. Adversarial / edge-case profiles
    # ------------------------------------------------------------------
    {
        # Conflict: user says "sad" mood but energy=0.9 (energetic)
        # Expected oddity: mood bonus fires on songs labelled 'sad'
        # (only "Birch and Bone") but numerical scores push high-energy
        # tracks to the top — the label and numbers fight each other.
        "_name": "EDGE: Sad but Energetic",
        "_description": "Conflicting prefs — sad mood label + high energy target",
        "favorite_genre":      "metal",
        "favorite_mood":       "sad",
        "target_energy":        0.90,
        "target_valence":       0.20,
        "target_acousticness":  0.10,
        "target_danceability":  0.50,
        "target_tempo_bpm":   170.0,
    },
    {
        # Dead-center on every numerical feature — perfectly average taste.
        # No song is a great match; no song is a terrible match.
        # Reveals whether the genre bonus alone can swing the ranking.
        "_name": "EDGE: Perfectly Average",
        "_description": "All targets at 0.5 midpoint — exposes genre bonus dominance",
        "favorite_genre":      "jazz",
        "favorite_mood":       "relaxed",
        "target_energy":        0.50,
        "target_valence":       0.50,
        "target_acousticness":  0.50,
        "target_danceability":  0.50,
        "target_tempo_bpm":   110.0,
    },
    {
        # Genre that does not exist in the catalog — genre bonus never fires.
        # Tests whether the system degrades gracefully to pure numerical ranking.
        "_name": "EDGE: Genre Not in Catalog",
        "_description": "Favorite genre 'k-pop' has zero songs — pure numerical fallback",
        "favorite_genre":      "k-pop",
        "favorite_mood":       "happy",
        "target_energy":        0.80,
        "target_valence":       0.90,
        "target_acousticness":  0.10,
        "target_danceability":  0.85,
        "target_tempo_bpm":   120.0,
    },
]


# ---------------------------------------------------------------------------
# Display helper
# ---------------------------------------------------------------------------

MAX_SCORE = 16.5  # EXPERIMENT: energy doubled (7.0), genre halved (1.0)
WIDTH     = 62


def print_recommendations(profile: dict, recommendations: list) -> None:
    name  = profile["_name"]
    desc  = profile["_description"]

    print()
    print("=" * WIDTH)
    print(f"  {name}")
    print(f"  {desc}")
    print("=" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        bar_filled = int((score / MAX_SCORE) * 20)
        bar = "#" * bar_filled + "-" * (20 - bar_filled)

        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre : {song['genre']:<12}  Mood : {song['mood']}")
        print(f"       Score : {score:5.2f} / {MAX_SCORE:.1f}  [{bar}]")

        reasons = explanation.split(", ")
        print(f"       Why   : {reasons[0]}")
        for reason in reasons[1:]:
            print(f"                {reason}")

    print()
    print("=" * WIDTH)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile in PROFILES:
        # Strip private _keys before passing to recommender
        user_prefs = {k: v for k, v in profile.items() if not k.startswith("_")}
        recs = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(profile, recs)


if __name__ == "__main__":
    main()
