# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This project builds a simple but functional music recommendation engine in Python. You give it a taste profile , your favorite genre, mood, and energy level and it scores every song in the catalog to find your best matches, explaining exactly why each one ranked where it did. It's a content-based filtering system, meaning it only looks at the song's own attributes rather than what other users listened to. 

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

Each song in the catalog has seven attributes: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`.

A user profile captures four preferences: `favorite_genre`, `favorite_mood`, `target_energy`, and whether they want acoustic or danceable music.

The recommender scores every song using a simple weighted formula:

- **+2.0 points** — genre matches your preference (strongest signal)
- **+1.0 points** — mood matches your preference
- **+0.0 to +1.0 points** — how close the song's energy is to your target (the closer, the more points)
- **+0.5 points** — danceability bonus if you want upbeat music and the song qualifies

Every recommendation also prints a reason string so you always know why a song ranked where it did , not just a score, but a plain-English breakdown like `genre match (+2.0) | mood match (+1.0) | energy similarity (+0.93)`.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

**Halving the genre weight (2.0 → 1.0)**
Rankings reshuffled almost completely. Energy became the dominant signal and songs from "wrong" genres started climbing to the top. It confirmed that genre is doing the heavy lifting in this system , more than I expected going in.

**Removing the mood feature entirely**
Surprisingly, the top results barely changed for most profiles. Genre and energy together were already enough to isolate the same cluster of songs. Mood turned out to be more of a tiebreaker than a primary driver.

**Adversarial profile — high energy but sad mood**
The system returned intense, aggressive tracks and completely ignored the emotional contradiction. It has no way to reconcile conflicting preferences, which is a real limitation.


---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

- The catalog is only 10 songs, so niche genres get zero matches almost immediately
- Genre matching is all-or-nothing , "indie" and "alternative" are treated as completely unrelated
- The system creates filter bubbles: pop fans will see the same 3–4 songs every time
- It has no memory ,it can't learn from skips, replays, or saves the way Spotify does
- It assumes one mood and one genre, which doesn't reflect how most people actually listen


---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

Building this made me realize how deceptively simple recommendation systems look from the outside. Three scoring rules, a sort, and a slice and yet it already has measurable biases and blind spots. The genre weight experiment was the most eye-opening part: one number controls more of the output than everything else combined, and you'd never know that without testing it.

It also changed how I think about Spotify and YouTube recommendations. Those platforms aren't just doing what I built here at a larger scale  they're solving fundamentally harder problems around implicit feedback, taste drift over time, and cold start users. Content based filtering is just the foundation. The interesting work happens on top of it.

See [model_card.md](model_card.md) for the full breakdown of strengths, limitations, and future ideas.



---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
**MoodQueue 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

MoodQueue 1.0 suggests up to five songs from a small curated catalog based on a user's preferred genre, mood, and energy level. It is built for classroom exploration , not for real streaming products or real users.

It assumes a user can be described by a single genre preference, a single mood, and one target energy value. It does not model complex or changing taste over time.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Imagine the recommender as a friend flipping through a stack of CDs for you. For each one they ask three questions:

1. **Is this the right genre?** A match earns the most points meaning genre is the strongest signal.
2. **Does this match my mood right now?** A mood match adds a solid bonus.
3. **How close is the energy to what I want?** A song that perfectly matches your target energy gets a full extra point. One that's way too loud or too quiet gets close to zero.
4. **Is it danceable?** If you want something to move to and the song qualifies, it gets a small bonus on top.

After scoring every song that way, the friend hands you the top five in order from best match to worst. Every pick comes with a short note explaining exactly which questions it answered well.


---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog contains 10 songs stored in `data/songs.csv`. Genres represented include pop, rock, lofi, EDM, and alternative. Moods include happy, chill, intense, energetic, and sad.

The dataset skews toward mainstream Western artists and reflects one curator's taste. Classical, jazz, K-pop, Latin, and R&B are completely absent, which means users who prefer those genres will get poor results since they'll never earn a genre-match bonus.


---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

- Works well for mainstream profiles. Pop, EDM, and rock users get highly relevant results because those genres are well represented in the catalog.
- Every recommendation comes with a plain-English explanation, so the user always knows *why* a song ranked where it did — not just a number.
- Fast and transparent. No black-box model, no external APIs. The entire logic fits in one file and runs in under a second.


---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  


- **Genre dominates everything.** At 2.0 points, a genre match outweighs every other signal combined. A pop fan who wants chill vibes will still mostly get pop, not lofi.
- **Underrepresented genres get ignored.** There are no classical, jazz, or K-pop songs. Users who prefer those genres score zero genre-match points and get semi-random energy-based results instead.
- **Binary matching.** "Indie" and "alternative" are treated as completely unrelated genres even though they overlap heavily in real life.
- **Single-preference model.** People rarely want exactly one mood. Someone who is mostly happy but a little nostalgic can't be expressed in this profile format.
- **No diversity enforcement.** The top five can easily be dominated by the same artist or genre if they happen to match every signal.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

Five distinct user profiles were tested: Happy Pop Fan, Chill Lofi Listener, High-Energy Rock, Sad Indie Night, and EDM Dance Floor. For each one I checked whether the top results matched my own intuition about what those users would actually want.

Four out of five felt right immediately. The Sad Indie Night profile was the weakest with no indie or sad songs in the catalog, it fell back entirely on energy similarity and returned lofi tracks instead, which aren't the same thing at all.

Two experiments were also run: halving the genre weight reshuffled almost every list, and removing the mood feature barely changed anything. That second result was genuinely surprising.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  


1. **Collaborative filtering layer** — add "users who liked this also liked…" signals to break out of pure content-based filter bubbles.
2. **Diversity penalty** — prevent the same artist or genre from appearing more than twice in the top results.
3. **Genre similarity graph** — treat "indie" and "alternative" as closer to each other than "lofi" and "metal" using a simple similarity matrix instead of exact string matching.
4. **Preference blending** — let users specify multiple genres or moods with individual weights, like 70% pop and 30% soul.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  


Building MoodQueue made it clear how much hidden complexity sits behind a simple "You might also like…" banner. Even with just three scoring rules the system showed real biases — genre dominated everything, niche users got ignored, and conflicting preferences caused nonsensical results.

The most unexpected moment was the mood-removal experiment. I assumed mood would be crucial, but genre and energy together were already enough to isolate the right cluster for most profiles. That taught me that feature importance is not intuitive — you have to test it to know.

It also changed how I think about Spotify. Their system isn't just doing what I built at a larger scale. They're solving fundamentally harder problems: learning from implicit signals like skips and replays, handling users whose taste changes over time, and introducing people to music they didn't know they'd love. A weighted score can give you more of what you already like. Getting you somewhere genuinely new still takes something more.
