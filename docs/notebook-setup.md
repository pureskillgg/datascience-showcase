# Notebook setup and reading local tomes

This repo's published package exists mainly to bootstrap a Jupyter notebook so it
can find and read a local PureSkill.gg **tome** data set. This doc explains the
moving parts. None of this touches the cloud — tomes are read from the local
filesystem.

## The flow

A notebook starts with three cells:

```python
from pureskillgg_datascience_showcase.notebook import setup_notebook
setup_notebook()
%load ../usual_suspects.py
```

1. `setup_notebook(silent=False)` calls `setup_env_from_dotenv()` then
   `echo_paths()`.
   - `setup_env_from_dotenv()` runs `load_dotenv(os.path.join("..", ".env"))`,
     i.e. it loads a `.env` file **one directory above the notebook** into the
     process environment.
   - `echo_paths()` prints the four tome-related variables so you can confirm the
     curator will look in the right place. Pass `setup_notebook(silent=True)` to
     skip the printout.
2. `%load ../usual_suspects.py` pulls in the shared boilerplate: pandas, numpy,
   matplotlib, display options, and the one line that matters —
   `curator = TomeCuratorFs()`.

`TomeCuratorFs` is the **filesystem** tome reader from `pureskillgg_dsdk.tome`
(the `Fs` suffix = local files, not S3). It reads its collection location from the
environment, which is why the `.env` must be loaded first.

## The environment variables

`env_setup.py` uses `ENV_PREFIX = "pureskillgg_tome"` and joins it with each name,
uppercased. So the variables it reads and echoes are:

| Echoed name          | Environment variable                     | Meaning |
| -------------------- | ---------------------------------------- | ------- |
| `default_header_name`| `PURESKILLGG_TOME_DEFAULT_HEADER_NAME`   | dsdk tome header name to use by default |
| `ds_type`            | `PURESKILLGG_TOME_DS_TYPE`               | data-set type for the curator |
| `collection_path`    | `PURESKILLGG_TOME_COLLECTION_PATH`       | path to the tome collection on disk |
| `ds_collection_path` | `PURESKILLGG_TOME_DS_COLLECTION_PATH`    | path to the data-set collection on disk |

A minimal `../.env` therefore points the curator at a local tome collection, for
example:

```dotenv
PURESKILLGG_TOME_COLLECTION_PATH=H:\CSDS_tomes\
PURESKILLGG_TOME_DS_COLLECTION_PATH=H:\CSDS_tomes\
PURESKILLGG_TOME_DS_TYPE=csds
PURESKILLGG_TOME_DEFAULT_HEADER_NAME=header
```

If a variable is unset, `echo()` prints `... is not setup`, which is the quickest
way to debug a notebook that fails to load data.

## Reading tomes two ways

### Pre-built named tome

The analysis notebooks read an already-rolled-up tome dataframe by name and date
range, for example:

```python
df = curator.get_dataframe('channel_player_disconnect.2021-05-01,2022-01-01')
df = curator.get_dataframe('channel_player_death.2022-04-01,2022-06-27.may-missing')
```

### Building a tome with reading instructions

The template notebook builds a tome on the fly with `make_tome`, selecting
specific channels and columns via `ds_reading_instructions`, then iterates pages:

```python
tomer = curator.make_tome(
    'counter_strafing',
    header_tome_name="subheader_tome_all",
    behavior_if_partial='continue',
    max_page_size_mb=1,
    ds_reading_instructions=[
        {"channel": 'player_info', "columns": ['player_id_fixed', 'rank', 'wins', 'round']},
        {"channel": 'weapon_fire', "columns": ['tick', 'weapon_name', 'player_id_fixed']},
        {"channel": 'header'},
        {"channel": 'player_vector', "columns": ['tick', 'player_id_fixed', 'z_vel', 'recoil_index', 'speed_2d', 'duck_amount']},
    ])

for data, key in tomer.iterate():
    df = extract_cool_df(data)
    tomer.concat(df)
```

## Gotchas

- `pureskillgg_datascience_showcase/env_functions/` has no `__init__.py`;
  `setup_notebook.py` imports it via `from ..env_functions.env_setup import ...`,
  relying on implicit namespace-package import.
- In the M4 notebook the raw `weapon_name` value `m4a1` is the **M4A4**, and
  `m4a1_silencer` / `m4a1_silencer_off` are the **M4A1-S**. The notebook renames
  them (`m4a4_kills` / `m4a1_kills`) to avoid confusion.
