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

A **tome** combines one kind of data from many matches into a few files that load in seconds. Build the **header tome** once: it has one row per match, with the map, date, platform and more. Then make a tome for each thing you want to plot.

```python
import pureskillgg_datascience_showcase as psgg

curator = psgg.curator()

# Once, and again after downloading more days
header = curator.create_header_tome()
print(len(header.get_dataframe()), "matches")

# Optional: a filtered view of the header, e.g. one map
curator.create_subheader_tome("subheader_mirage", lambda df: df["map_name"] == "de_mirage")

# A tome of every death on Mirage, with only the columns you need
tomer = curator.make_tome(
    "deaths_mirage",
    header_tome_name="subheader_mirage",
    ds_reading_instructions=[
        {"channel": "player_death", "columns": ["round", "weapon_name", "player_x_pos", "player_y_pos",
                                                "player_z_pos", "attacker_team_code"]},
    ],
)
for data, key in tomer.iterate():
    df = data["player_death"]
    df["match"] = key
    tomer.concat(df)

deaths = curator.get_dataframe("deaths_mirage")
```

- **Work out the transform on one match first:** `curator.get_match_by_index(0).get_channels()`. Then move it into the loop.
- **Read only what you need.** `ds_reading_instructions` picks channels and columns, and building is much faster for it.
- **A tome can't grow once it's finished.** To add days, build it again under a new name. A common convention puts the dates in the name: `deaths_mirage.2026-08-01,2026-08-08`.
- **Older revisions have fewer channels.** Days before 2026-08-04 have 30 files per match instead of 42, so a channel you ask for may be missing. The [archived spec](https://docs.pureskill.gg/datascience/old/cs2/csds/spec) lists what they had.

Next: [the data primer](data-primer.md) covers what's in a match, and the traps to avoid when you plot it.
