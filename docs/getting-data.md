# Getting the data

The data is the **PureSkill.gg Competitive CS2 Gameplay** data set, published on the AWS Data Exchange. It is free to subscribe to, but it needs our approval, and moving it around costs standard AWS fees. You subscribe, export days of data to your own S3 bucket, download them into a folder, and then build *tomes*: small tables made from many matches, which is what you'll actually plot.

[docs.pureskill.gg](https://docs.pureskill.gg/datascience/) is the reference for the data set itself: the license, costs, retention and the [spec of every channel and column](https://docs.pureskill.gg/datascience/adx/cs2/csds/spec). This page only walks you through the steps.

## 1. Subscribe

Subscribe on the [product page](https://aws.amazon.com/marketplace/pp/prodview-v3o7zrt6okwmo). Say what you want to make; approval takes a few days, and we may email you first.

You agree to the Data Subscriber Agreement when you subscribe. In short, it's CC BY-NC-SA 4.0:
- no commercial use;
- attribute PureSkill.gg: `psgg.save()` puts "Data provided by PureSkill.gg." on every image for you;
- share what you derive from the data under the same license.

## 2. Set up AWS credentials

dsdk talks to AWS through boto3. Follow boto3's [credentials guide](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration) so `aws sts get-caller-identity` works.

## 3. Export days to your S3 bucket

Each *revision* of the data set is one day of matches, and the data set keeps about the last year. Find your **data set ID** in the AWS console: Data Exchange → Entitled data → the PureSkill.gg product → the data set → Data set ID.

```python
from pureskillgg_dsdk import export_multiple_adx_dataset_revisions_to_s3

export_multiple_adx_dataset_revisions_to_s3(
    "my-bucket",          # a bucket you own
    "<data set ID>",
    start_date="2026-08-01",
    end_date="2026-08-08",  # one week
)
```

**This costs money, on your AWS bill.** Start with a few days. As of August 2026, one match is about 35 MB in 43 objects, and a day is 90 to 150 matches. The [cost FAQ](https://docs.pureskill.gg/datascience/#cost-faq) has the numbers and how to keep them down.

## 4. Download into a folder

Sync from S3, **keeping the path structure**: the folders below `csds/` are part of each match's key, and dsdk won't find the matches without them.

```sh
aws s3 sync s3://my-bucket/csds/2026/08/ ~/pureskill-data/csds/2026/08/ \
  --exclude "*player_vector" --exclude "*player_status"
```

The two `--exclude`s skip the per-tick telemetry, which is most of every match's size. Leave them out if you need positions tick by tick (for movement trails, say). Deaths, damage, grenades and shots (`player_death`, `player_hurt`, `grenade_state`, `weapon_fire`) carry positions of their own, so they work without it.

## 5. Point the repo at it

Copy `.env.example` to `.env` at the repo root (git ignores `.env`) and fill it in:

```dotenv
# The folder that contains csds/
PURESKILLGG_TOME_DS_COLLECTION_PATH=/home/you/pureskill-data
# Where your tomes go; any folder
PURESKILLGG_TOME_COLLECTION_PATH=/home/you/pureskill-tomes
PURESKILLGG_TOME_DS_TYPE=csds
PURESKILLGG_TOME_DEFAULT_HEADER_NAME=header
```

`psgg.load_env(verbose=True)` prints what it found. It finds `.env` from any folder in the repo, so a notebook in `gallery/<item>/` works too.

## 6. Build tomes

A **tome** combines one kind of data from many matches into a few files that load in seconds. `build_basic_tomes` builds them in one pass over your matches: the **header tome**, with one row per match (the map, date, platform and more), and one tome for each channel you name, with every row tagged with its match in `match_key`.

```python
import pureskillgg_datascience_showcase as psgg

curator = psgg.curator()

# Every death, with only the columns you need. This builds the header tome too.
basic = curator.build_basic_tomes([
    {"channel": "player_death", "columns": ["round", "weapon_name", "player_x_pos", "player_y_pos",
                                            "player_z_pos", "attacker_team_code"]},
])
header = basic.header.get_dataframe()
deaths = basic.tomes["player_death"].get_dataframe()
print(len(header), "matches,", len(deaths), "deaths,", basic.dates)

# Mirage only: match_key is the header's `key`
mirage = header.loc[header["map_name"] == "de_mirage", "key"]
deaths_mirage = deaths[deaths["match_key"].isin(mirage)]
```

- **Names:** each channel's tome is called `basic_<channel>.<first day>,<last day>`, like `basic_player_death.2026-08-01,2026-08-08`. Load it again later with `curator.get_dataframe(name)`.
- **See what's already built:** `psgg.list_tomes()` returns each tome with its page count. A tome with 0 pages is empty or unfinished, and `get_dataframe` fails on it with `The tome has no pages`.
- **Read only what you need.** A whole channel works too (`"player_death"`), but naming columns makes building much faster and the tome smaller.
- **Days from different revisions mix fine.** Older days store some flags as 0 and 1 (in `player_death`, `player_status`, `other_death` and `bomb_defuse`), newer days as true and false. `build_basic_tomes` reads them all as true and false.
- **A tome is found by its name, not its columns.** Ask again for the same channel and days with different columns, and you get the finished tome back with its old columns. Give each set of columns its own name, as in `tome_name="weapons_{channel}.{dates}"`, or rebuild with `behavior_if_complete="overwrite"`.
- **Running it again is cheap.** A finished tome is kept, so a second call with the same channels reads nothing. A tome can't grow, though: after downloading more days, pass a new header name, such as `header_tome_name="header.2026-08-01,2026-08-15"`. The header is then scanned again, and the channel tomes get the new dates in their names.
- **Older revisions have fewer channels.** Days before 2026-08-04 have 30 files per match instead of 42, so a channel you ask for may be missing. The [archived spec](https://docs.pureskill.gg/datascience/old/cs2/csds/spec) lists what they had.

### When each match needs your code first

`make_tome` runs your own code on every match before it's stored. Use it when the raw rows are too big to keep and you only need a summary of each match. `player_vector`, for one, has a row per player per tick. This keeps each player's share of ticks spent ducked, per round:

```python
tomer = curator.make_tome(
    "ducked_by_round.2026-08-01,2026-08-08",
    ds_reading_instructions=[{"channel": "player_vector", "columns": ["round", "player_id_fixed", "is_ducked"]}],
)
for data, key in tomer.iterate():
    df = data["player_vector"].groupby(["round", "player_id_fixed"], as_index=False)["is_ducked"].mean()
    df["match_key"] = key          # the match, same as the header tome's `key` column
    tomer.concat(df)

ducked = curator.get_dataframe("ducked_by_round.2026-08-01,2026-08-08")
```

- **Work out the transform on one match first:** `curator.get_match_by_index(0).get_channels()` gives one match's channels. Then move the code into the loop.
- **Flags break `make_tome` across revisions.** It joins each page's matches with pandas, so a page mixing 0/1 flags with true/false ones fails with `ArrowInvalid: Could not convert 0 with type int: tried to convert to boolean`. Leave those flag columns out, or convert them in the loop: `df[flags] = df[flags].astype("boolean")`.

Next: [the data primer](data-primer.md) covers what's in a match, and the traps to avoid when you plot it.
