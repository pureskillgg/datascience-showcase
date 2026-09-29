# Contributing

Made something good with the data? Add it to the gallery.

## Add a graphic to the gallery

1. Fork the repo and set it up (see the [README](README.md)).
2. Copy `templates/gallery-item/` to `gallery/<your-slug>/`, with a short slug of lowercase words and hyphens.
3. Make the graphic with the kit, in `make.py` or the notebook, and save the image with `psgg.save()`. The gallery check only accepts PNGs saved that way.
4. Fill in your item's `README.md`:
   - `title`
   - `author`: your name or GitHub handle
   - `official: false`
   - `data`: which matches and dates
   - `image`
   - a few lines on what it shows
5. Run `make gallery`, then `make check`, `make lint` and `make test`.
6. Open a pull request.

**Videos:** post them on YouTube or similar, commit a still frame, and put the link in `video:`. Video files aren't accepted.

**Community graphics are never official.** Keep `official: false`, and don't add the PureSkill.gg logo, `official=True` included. Official means PureSkill.gg made it.

## What we check

- The image is a stamped PNG with the attribution line, "Data provided by PureSkill.gg."
- The script or notebook rebuilds it from a tome, with no data committed. Nothing from the data set goes in the repo except the images.
- It follows the [style guide](docs/style.md), which the kit does for you if you don't override it.
- The README says which data it uses.

## Licenses

- **Code** you contribute is under the repo's [MIT license](LICENSE.txt).
- **Graphics** made from the PureSkill.gg data set are derived from it, so the data license applies to them: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), through the Data Subscriber Agreement. That means non-commercial, attributed, and shared under the same terms.

## Changes to the kit

Open an issue first for anything that changes the look (colors, fonts, presets, layout); that's the PureSkill.gg brand. Fixes and new helpers are welcome as pull requests with tests.

Questions: the Dojo channel on [Discord](https://pureskill.gg/discord), or contact@pureskill.gg.
