"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs  # python -m src.main
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs      # python src/main.py


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile: a late-night focused worker who likes calm, slightly melancholic
    # electronic/lofi sounds — low energy, moderate danceability, mostly synthetic.
    user_prefs = {
        "favorite_genre": "lofi",       # preferred genre for genre-match bonus
        "favorite_mood":  "chill",      # preferred mood label
        "target_energy":      0.40,     # calm, not silent — background listening
        "target_valence":     0.55,     # slightly positive but not upbeat
        "target_acousticness": 0.70,    # prefers organic/warm textures
        "target_danceability": 0.60,    # gentle groove, not a dance floor
        "target_tempo_bpm":   80.0,     # slow-to-mid BPM
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    max_score = 13.0
    width = 60

    print()
    print("=" * width)
    print(" MUSIC RECOMMENDER — TOP 5 PICKS FOR YOU")
    print("=" * width)
    print(f"  Profile : {user_prefs['favorite_genre'].upper()} / "
          f"{user_prefs['favorite_mood']} / "
          f"energy {user_prefs['target_energy']}")
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        bar_filled = int((score / max_score) * 20)
        bar = "#" * bar_filled + "-" * (20 - bar_filled)

        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre: {song['genre']:<12}  Mood: {song['mood']}")
        print(f"       Score: {score:5.2f} / {max_score:.1f}  [{bar}]")
        print(f"       Why  : ", end="")

        # Print each reason on its own indented line
        reasons = explanation.split(", ")
        print(reasons[0])
        for reason in reasons[1:]:
            print(f"               {reason}")

    print()
    print("=" * width)
    print()


if __name__ == "__main__":
    main()
