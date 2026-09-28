# Data primer and field notes

A short orientation, then the traps that make a chart quietly wrong. For every channel and column, see the [CSDS spec](https://docs.pureskill.gg/datascience/adx/cs2/csds/spec); this page doesn't repeat it.

## What's in a match

- **A match is a folder**, `csds/<yyyy>/<mm>/<dd>/<match>/`. It holds `csds`, a gzipped JSON index (the *manifest*), and one parquet file per *channel*, with no file extension.
- **Each channel is one table.** Most are one row per game event: `player_death`, `player_hurt`, `weapon_fire`, `grenade_state`, `round_end` and so on. `player_vector` and `player_status` are per-tick telemetry. `header` is one row about the match: map, date, platform, tick rate.
- **Players are `player_id_fixed`**, stable for the whole match. Names and Steam IDs are redacted.
- **Merged columns.** Many event channels carry the acting player's state at that tick, prefixed `player_` and `attacker_`: position, velocity, view angles, weapon and team. You rarely need to join telemetry yourself.
- **A tome** is your own table built across many matches ([getting data](getting-data.md)). Charts come from tomes, not from raw matches.

## Field notes

### Sides, teams and rounds

- **Team codes: 2 is T, 3 is CT** (`*_team_code`, `winner_team_code`). `psgg.side_color(2)` gives the T color.
- **Sides swap at halftime.** A player's team code changes after round 12, so group by side per round, not per player.
- **Regulation is 24 rounds** (MR12): pistol rounds are 1 and 13, and overtime is rounds 25 and up, in sets of six. Old CS:GO rules (30 rounds) don't apply.
- **`player_spawn.round` is one behind.** A spawn is labelled with the round that just ended, and round 1's spawn is missing. Shift it by one before joining per-round data.
- **`score_update` double-counts at halftime.** It mixes round wins with side-swap rows. Take round winners from `round_end.winner_team_code`.

### Positions and maps

- **Positions are world units** (`x_pos`, `y_pos`, `z_pos`; about 1 unit to the inch). Map graphics convert them with `psgg.maps.to_radar(map_name, x, y)`, using Valve's overview numbers for that map.
- **Nuke, Vertigo, Train and Baggage have two floors.** Split by height with `psgg.maps.level_of(map_name, z)` and draw each floor on its own radar, or deaths on one floor land on top of the other.
- **Velocity spikes at respawn.** The first sample after a player respawns divides the teleport distance by one tick, giving speeds in the hundreds of thousands. Drop speeds above about 3,500 units/s, or the first sample of each player in each round.
- **Positions can fall out of the world.** `world_item_vector` items that drop through the map reach the engine floor, z of about −16,384.

### Angles

- **`theta_ang` is yaw** (where the player faces, −180 to 180) and **`phi_ang` is pitch** (1 to 179, with 90 level and larger looking down). The names are the reverse of the physics convention, so don't trust them.

### Weapons

- **`m4a1` is the M4A4.** The M4A1-S is `m4a1_silencer` (and `m4a1_silencer_off` when the silencer is off). Label them, or the M4A4 and M4A1-S swap.
- **Other names that trip people:** `usp_silencer` is the USP-S, `hkp2000` the P2000, `inferno` the fire from a molotov or incendiary, `hegrenade` the HE grenade.
- **Weapon names aren't the same in every channel.** `item_equip`, `item_pickup`, `weapon_fire` and `item_refund` use different vocabularies; check the values before you join on them.

### Time

- **Tick rate is 64 per second** in CS2 (`header.tick_rate`), and every row has a `second` computed from its tick. Ignore `header.tick_save_rate`: it says 21, but the data is saved at 64.

### Values that mean "missing"

- **`attacker_id` 65535 means no attacker** (the world, the bomb, fall damage). The matching `attacker_id_fixed` is empty.
- **`*_id_fixed` columns can load as floats** in some matches, when a row has no player. Cast them with `.astype("Int64")` before you join or compare.
- **`molotov_state` uses −1 and −2 for "unknown"** in `player_id` and `extinguisher_id`, and 0 is a real player there.
- **`site_code` isn't A or B.** It's an arbitrary per-map number that can differ between matches of the same map. Use positions, or the bomb plant's position, to tell the sites apart.

### Ranks

- **Two rank scales share the same columns.** Premier CS Rating (up to about 20,000) and the competitive skill groups (0 to 18). `player_info.rank_type` tells them apart: 11 is Premier, 12 is competitive. Never average them together.
