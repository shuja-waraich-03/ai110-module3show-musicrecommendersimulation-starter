# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

VibeFinder 1.0 is a classroom simulation — it is not a production product. It is designed for a single user who fills in a hand-coded taste profile (their preferred genre, mood, energy level, and other features), and the system returns the five best-matching songs from an 18-song catalog.

The system assumes the user can accurately describe their own taste as numbers (e.g., "my target energy is 0.90"). In the real world most people cannot, and would need a listening history or rating system to infer those values. This simulation skips that step to focus on the scoring logic itself.

**This system should not be used** to make music decisions for real listeners, to represent any group's preferences, or in any context where bias or coverage gaps could cause harm. It is strictly for educational exploration of how content-based recommendation algorithms work.

---

## 3. How the Model Works  

Every song in the catalog is described by seven features: its genre (like "rock" or "lofi"), its mood label (like "chill" or "intense"), and five numbers — energy (how intense it feels), valence (how happy it sounds), acousticness (how organic vs. electronic), danceability (how rhythmic), and tempo in beats per minute.

The user provides a matching set of targets: their favorite genre, favorite mood, and ideal values for each of those five numbers.

For every song, the system computes a score in two steps:

**Step 1 — Label bonuses.** If the song's genre exactly matches the user's favorite genre, the song earns a bonus point. If the mood label also matches, it earns another bonus point. These are all-or-nothing: partial matches get nothing.

**Step 2 — Proximity scores.** For each of the five numbers, the system measures how close the song is to the user's target using a bell-curve formula. A song that exactly matches the target earns the full weight for that feature. A song that is far away earns almost nothing. Each feature has a different weight reflecting how much it should matter: energy carries the most weight (it sets the overall vibe), followed by valence (emotional tone), then acousticness and danceability (texture and groove), then tempo (which listeners tolerate variation in the most).

The five proximity scores plus the two label bonuses are added together. The five songs with the highest totals are returned as recommendations, along with a plain-language explanation of which features contributed most.

The main change from the starter code was the weight-shift experiment: energy was doubled from 3.5 to 7.0, and the genre bonus was halved from +2.0 to +1.0. This made energy even more dominant in the ranking.

---

## 4. Data  

The catalog contains **18 songs**, all hand-crafted for this simulation. The songs were not pulled from a real streaming service — every feature value (energy, valence, etc.) was assigned manually to create a spread of different listening profiles.

**Genres represented:** lofi (3 songs), pop (2), ambient (2), synthwave (1), hip-hop (1), jazz (1), R&B (1), classical (1), country (1), metal (1), reggae (1), folk (1), blues (1), and rock (1).

**Moods represented:** chill (3), happy (3), intense (3), moody (2), relaxed (1), romantic (1), nostalgic (1), energetic (1), sad (1), and uplifting (1) — though not all of these are evenly represented.

I expanded the catalog from the 10-song starter set by adding 8 more songs spanning hip-hop, R&B, classical, country, metal, reggae, folk, and blues. The goal was to cover a wider range of genres so that adversarial profiles (like a metal or k-pop listener) would expose gaps in the scoring logic.

**What's missing:** No k-pop, Latin, EDM, or global music. Only one song per most genres, meaning the catalog strongly favors lofi listeners (who get 3 songs) over everyone else. The feature values reflect a Western pop-music frame: "high valence = happy" may not translate across all musical traditions.

---

## 5. Strengths  

**Specific listeners get accurate results.** When a user's taste profile is tight and specific — like the Chill Lofi profile, which has a clear energy target (0.40), high acousticness preference (0.70), and a slow BPM target (80) — the system returns results that genuinely match. The top three lofi songs appear every single run, and there is a clear score gap between #3 and #4, meaning the system is confident rather than guessing.

**The scoring is transparent.** Every recommendation comes with a reason string that shows exactly which features contributed and by how much (e.g., "energy very close to target (+3.49/3.5)"). Unlike a black-box neural network, anyone can see why a song ranked where it did. This transparency is a major practical advantage for a small, explainable system.

**Graceful degradation when genres are missing.** When a user's favorite genre is not in the catalog (the k-pop adversarial profile), the system does not crash or return garbage — it simply falls back to pure numerical ranking. Sunrise City (pop) emerged as #1 because its features were numerically closest, which is a reasonable substitute even if the label is wrong.

**The Gaussian formula avoids hard cliffs.** Because proximity is calculated with a bell-curve rather than a threshold (e.g., "within 0.2 or nothing"), songs that are close-but-not-perfect still earn partial credit. This produces a natural ordering rather than large groups of songs that all score the same.

---

## 6. Limitations and Bias 

**The energy filter bubble is the most serious structural flaw.** Because energy carries the highest weight (7.0 in the experimental version, 3.5 in the baseline), a song whose energy differs from the user's target by more than ~0.5 units earns almost nothing from that feature — a high-energy song (0.97) scoring against a chill profile (target 0.40) receives only 0.52 out of a possible 7.0 points from energy alone. This means a chill-profile user will essentially never see an intense or high-energy song in their top 5, even if that song matches their preferred genre, mood, danceability, and tempo perfectly. Real listeners often want variety — a lofi fan might love one high-energy song for a workout — but this system has no way to surface that.

**Genre coverage is thin and unequal.** Lofi is the only genre with more than one song (3 of 18, or 17%), which means a lofi user consistently sees the same 3 songs at the top of every run regardless of how the other features vary. Fifteen other genres each have exactly one representative, so any user who prefers country, reggae, blues, or folk will receive at most one genre-bonus point in the entire catalog — making those profiles effectively second-class compared to lofi listeners.

**Mood labels are coarse and unevenly distributed.** Three moods — happy, chill, and intense — each appear on 3 songs (17% each), while 8 other moods appear on only 1 song each. A user whose favorite mood is "romantic," "nostalgic," or "sad" has only one possible mood-bonus song in the entire catalog, meaning that +1.0 bonus almost never fires. Meanwhile, the mood label itself is imprecise: "chill" is applied to lofi, ambient, and one folk-adjacent track, so the bonus can reward songs that feel very different in practice.

**The system has no diversity mechanism.** Because it ranks purely by score, it will always return the top-k closest songs — even if those songs are nearly identical. In practice this means a chill-lofi user always receives Midnight Coding, Library Rain, and Focus Flow as their top 3, which are three songs by the same two artists with nearly identical feature vectors. A real recommender would inject diversity to prevent this kind of redundancy.

**Preferences are declared, not learned.** The user profile is hand-coded at launch and never updates. If a user's mood changes mid-session, or if their stated preferences do not match what they actually enjoy, the system has no mechanism to adapt. This is a fundamental limitation of content-based filtering without any feedback loop.

---

## 7. Evaluation  

I tested six user profiles in total — three standard profiles designed to represent real listener types, and three adversarial profiles designed to expose cracks in the scoring logic.

**Standard profiles tested:**

*High-Energy Pop* — a user who wants loud, fast, danceable pop music. The system correctly placed Sunrise City at #1 because it matched genre (pop), mood (happy), and came close on energy (0.82 vs target 0.90) and valence (0.84 vs target 0.85). What surprised me was that Gym Hero — which actually has higher energy (0.93) and better danceability — ranked second, not first. The reason is that Gym Hero's mood is labelled "intense" rather than "happy," so it missed the +1.0 mood bonus. A single label difference outweighed being a numerically closer match on four features. To a non-programmer: it's like a store clerk ignoring the product you actually want because the box says "workout" instead of "party," even though the contents are almost identical.

*Chill Lofi* — a late-night focus listener. This profile behaved almost exactly as expected: the three lofi songs (Midnight Coding, Library Rain, Focus Flow) occupied the top three spots every single run. What surprised me was how wide the gap was between #3 and #4. Focus Flow scored 11.92 while Spacewalk Thoughts (ambient, chill) scored 9.60 — a gap of 2.3 points — purely because Focus Flow has the genre bonus and Spacewalk Thoughts does not, even though both songs feel very similar to listen to.

*Deep Intense Rock* — a workout or commute listener who wants heavy, fast music. Storm Runner ranked first as expected, scoring nearly perfectly (12.87/13.0). The interesting result was #4: Night Drive Loop (synthwave, moody) appeared over Block Party Anthem (hip-hop, energetic). Synthwave is not rock, and moody is not intense, but its numerical features — especially valence and danceability — happened to land close to the rock profile's targets. This is the system finding a "numerically similar" song that most rock fans would not actually enjoy.

**Adversarial profiles tested:**

*Sad but Energetic* — a user who claims to want sad-mood, high-energy music. This profile exposed the conflict between labels and numbers directly. The only sad-labelled song in the catalog (Birch and Bone, folk, energy 0.31) never appeared in the top 5 because its energy was so far from the target (0.90) that the numerical penalty destroyed any mood-label advantage. The top results were all high-energy songs with dark valence — the system found the right *feeling* through numbers but could not honor the stated mood label.

*Perfectly Average* — all targets set to exactly 0.5 on every feature. This was designed to see whether the genre bonus alone could dominate the ranking. Coffee Shop Stories (jazz, relaxed) won every time with both the genre and mood bonus firing, scoring 10.75 against a field where most songs scored between 8 and 9. This confirms that in a tie-like scenario, categorical labels are the tiebreaker — which may not reflect how a real listener with genuinely average taste would respond.

*Genre Not in Catalog* — a user whose favorite genre (k-pop) does not exist in the catalog. The system degraded gracefully: it ignored the genre bonus entirely and ranked purely by numerical fit, placing Sunrise City first because its energy, valence, danceability, and tempo were all close to the target. This is the correct behavior, but it reveals that such a user is permanently disadvantaged — they can never receive the genre bonus that lofi or pop listeners enjoy on almost every run.

---

## 8. Future Work  

**Add a diversity filter.** The biggest quick win would be preventing the top-k results from being nearly identical songs. A simple re-ranking step could say: "if two songs have nearly the same feature vector, only keep the higher-scoring one and replace the other with the next most different song." This would stop the Chill Lofi profile from always returning three almost-identical lofi tracks.

**Expand the catalog and even out genre coverage.** Adding 3–5 songs per genre would eliminate the structural advantage lofi listeners have today. It would also make the system more useful to the broader range of music tastes that real listeners actually have — right now, 8 out of 14 genres have only a single representative.

**Replace declared preferences with inferred ones.** The most impactful improvement would be replacing the hand-coded user profile with a listening history. After each recommendation, the user could say "liked it" or "skip" — and the system could gradually shift the target values toward what they actually respond to, rather than what they said they wanted. This closes the gap between stated preferences and revealed preferences, which is the central flaw of this version.

**Add a "mood journey" feature.** Real listeners don't want the same energy level for 60 minutes. A future version could let users specify a mood arc (e.g., "start mellow, peak at 30 minutes, wind down") and sequence songs across that arc instead of returning five independent closest matches.

---

## 9. Personal Reflection  

The biggest thing this project taught me is how much work a label does compared to a number. I expected the numerical scores — energy, valence, tempo — to carry the recommendations, and they do. But mood and genre labels punch above their weight. A single label mismatch (a song tagged "intense" instead of "happy") can cost a song its top ranking even when every number is a near-perfect match. That surprised me: real listening apps like Spotify probably have the same issue hiding inside more complex models, just scaled up to millions of songs.

The weight-shift experiment was the most instructive part. I doubled energy's weight expecting to see the rankings scramble. Instead, the top result barely changed across any profile, because energy was already dominant enough to lock in the winner. What shifted was the gap between #1 and #2 — the leader just pulled further ahead. That taught me that changing a weight doesn't always change who wins; it changes how confident the system is, which is a different and subtler effect.

The adversarial profiles — especially "Sad but Energetic" and "Genre Not in Catalog" — changed how I think about fairness. Both profiles are realistic listener types: someone going through a breakup wants dark but intense music; K-pop fans are a massive audience. But the system silently disadvantages both of them — one because its label contradicts its numbers, the other because the catalog was never built for it. I now see that every time Spotify or YouTube "doesn't quite get" what someone wants, it might not be a bug in the algorithm — it might be a gap in the training data or a mismatch between how the system represents taste and how the listener actually experiences it.

Building this from scratch also made me appreciate how much real recommendation systems must be doing behind the scenes. This one has 18 songs, 7 features, and hand-coded weights — and it still produces results that take real analysis to explain. At a million songs and hundreds of features, the same tradeoffs (weight dominance, label coarseness, catalog gaps) would be nearly invisible until they started affecting entire communities.
