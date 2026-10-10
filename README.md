# Numbo

A daily speed-maths game. Ten sums, three levels, one clock. Built to match Glotto.

## Files

| File | What it's for |
|---|---|
| `index.html` | The whole game — markup, styling and logic in one file |
| `about.html` | The about page, linked from the footer |
| `build_site.py` | Builds `dist/`, the obfuscated version you upload |
| `favicon.ico`, `icon-*.png`, `apple-touch-icon.png` | Icons |

There is no data file or spreadsheet. The sums are generated in the browser from the day
number and the level, so every future day already exists.

## Try it right now

Double-click `index.html`. One quirk when running this way: browsers block clipboard
access on `file://` pages, so "Challenge a friend" falls back to a pop-up you copy from by
hand. It works normally once the site is hosted.

## Before you launch

Two settings in the `CONFIG` block at the top of the script in `index.html`:

```js
launchDate: "2026-10-05",   // day 1
siteUrl: "",                // your address, once you have a domain
```

- **`launchDate`** is day 1. It's set so that 10 October 2026 is day 6, leaving days 1–5
  as past puzzles. If you go live on a different date and still want to open on day 6, set
  it to five days before that date.
- **`siteUrl`** is the link put in the share text. Left blank it uses whatever address the
  page is served from, which is fine on GitHub Pages.

**Don't change `launchDate`, `MODES` or the generator after launch.** All three decide
which sums land on which day, so anyone mid-streak would see things shift, and old
challenge links would point at different sums.

## Building the version you upload

```bash
npm install javascript-obfuscator   # once
python build_site.py                # before every deploy
```

Upload the contents of `dist/`, exactly as with Glotto. Because the sums are generated in
the page, anyone determined can work out tomorrow's. That's harmless while results only
go between friends; it would matter if you ever add a public leaderboard.

## How it works

- **Rollover:** midnight UK time for everyone, same as Glotto.
- **Sums:** five add-or-subtract and five multiply-or-divide per level, shuffled. Every
  number is at least 2, divisions come out whole, subtractions never go negative, and no
  sum repeats within a day. The ranges live in `MODES`.
- **One attempt:** the start time is saved the moment Start is pressed, so reloading or
  leaving the page doesn't stop the clock or allow a second go.
- **Skips:** +10 seconds each (`skipPenalty`).
- **Medals:** under 30 / 45 / 60 / 90 seconds, the same on every level (`MEDALS`).
- **Challenge links:** `?d=6&m=h&t=41300&k=1` — day, level, time in milliseconds, skips.
  Opening one takes the player to that day and level and compares times at the end.
  Challenge links to past days skip the wait.
- **Past puzzles:** today and any day already started open straight away; an untouched
  past day goes through the ten-second wait (`gateSeconds`). As in Glotto, `gate()` is
  the placeholder for a rewarded ad.
- **Stats:** kept per level in `localStorage` under `numbo.results.v1` and worked out from
  the saved results each time. Past-puzzle plays count towards totals and medals but not
  streaks.

## Not included yet

A privacy page. Glotto's names its host, analytics and contact address, so Numbo's needs
writing once those are decided for the new site.
