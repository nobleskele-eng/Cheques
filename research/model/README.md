# Success model: how to re-run and add your research

## Run it
```
python3 research/model/success_model.py
```
- **Needs:** `numpy`. In the cloud session: `pip install numpy`.
- **Run time:** a few seconds.
- **It overwrites:**
  - `research/success-model.md`: the report.
  - `research/model/results.json`: all the numbers.

## Add your own research
Create **`research/data/extra_features.csv`**. The model picks it up automatically on the next run.

**Rules:**
- **First column must be `video_id`**, matching the IDs in `research/data/*_videos.csv`, from either account.
- **Every other column becomes a feature.**
  - **Numbers** (e.g. `brightness`, `seconds_of_rain`) are used directly. A column of only 0/1 is treated as yes/no.
  - **Text** (e.g. `location`, `opening_move`, `footage_source`) is turned into categories.
    - Each value that appears on 10+ videos becomes its own yes/no feature.
    - The most common value is the baseline the others are compared against.
    - Rarer values are ignored.
- **Blank cells are fine.** They're filled with the average, so you don't need every video labelled. But a feature only means something if it's labelled on a decent number of videos (aim for 50+).

**Example:**
```
video_id,location,opening_move,footage_source,has_dialogue
7692701610669100308,china,tilt_up,self_filmed,1
7691278649022057749,hong_kong,whip_pan,self_filmed,0
7695629231639825665,hong_kong,pan,self_filmed,0
```

The 8 videos already broken down in `replication-levers-and-encoding.md` §2.6 can be your first rows.

## What the report will and won't tell you
- **Will:** per-video odds of beating the account's weekly median, reaching 100K+, and reaching 1M+. You also get a held-out test of whether each is actually predictable.
- **Won't:** the chance that a *new account* succeeds. There are no failed accounts in the data.

The way to get that is to log your own first 60–120 posts in the same CSV format and add your account to `ACCOUNTS`, with its start date in `TAKEOFF`, in the script.
