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

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
