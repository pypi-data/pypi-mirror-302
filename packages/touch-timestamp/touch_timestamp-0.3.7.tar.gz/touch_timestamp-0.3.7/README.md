[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Change files timestamp with a dialog window.

![Gui window](https://github.com/CZ-NIC/touch-timestamp/blob/main/asset/mininterface-gui.avif?raw=True "Graphical interface")

GUI automatically fallback to a text interface when display is not available.

![Text interface](https://github.com/CZ-NIC/touch-timestamp/blob/main/asset/textual.avif?raw=True "Runs in the terminal")


# Installation

Install with a single command from [PyPi](https://pypi.org/project/touch-timestamp/).

```bash
pip install touch-timestamp
```

# Docs

## Methods to set the date

When invoked with file paths, the program sets their modification times
* to the specified time
* to the date from the Exif through [jhead](https://github.com/Matthias-Wandel/jhead)
* to a relative time
* to the specific time, set for a file, then shifts all the other relative to this

![Gui window](https://github.com/CZ-NIC/touch-timestamp/blob/main/asset/mininterface-gui-full.avif?raw=True "Graphical interface")

## Fetch the time from the file name

Should you end up with files that keep the date in the file name, use the `--from-name` parameter.

```bash
$ touch-timestamp 20240828_160619.heic --from-name True
Changed 2001-01-01T12:00:00 → 2024-08-28T16:06:19: 20240828_160619.heic
```

## Full help

Use the `--help` to see full options.

```bash
$ touch-timestamp --help
usage: Touch [-h] [--eel | --no-eel] [--from-name {True,False}|STR]
             [[PATH [PATH ...]]]

╭─ positional arguments ─────────────────────────────────────────────────────╮
│ [[PATH [PATH ...]]]                                                        │
│     Files the modification date is to be changed. (default: )              │
╰────────────────────────────────────────────────────────────────────────────╯
╭─ options ──────────────────────────────────────────────────────────────────╮
│ -h, --help                                                                 │
│     show this help message and exit                                        │
│ --eel, --no-eel                                                            │
│     Prefer Eel GUI. (Set the date as in a chromium browser.)               │
│     Does not allow setting from EXIF and relative set. (default: False)    │
│ --from-name {True,False}|STR                                               │
│     Fetch the modification time from the file names stem. Set the format   │
│     as for `datetime.strptime` like '%Y%m%d_%H%M%S'.                       │
│     If set to True, the format will be auto-detected.                      │
│     If a file name does not match the format or the format cannot be       │
│     auto-detected, the file remains unchanged.                             │
│                                                                            │
│                                                                            │
│     Ex: `--from-name True 20240827_154252.heic` → modification time =      │
│     27.8.2024 15:42 (default: False)                                       │
╰────────────────────────────────────────────────────────────────────────────╯
```


## Krusader user action

To change the file timestamps easily from Krusader, import this [user action](extra/touch-timestamp-krusader-useraction.xml): `touch-timestamp %aList("Selected")%`