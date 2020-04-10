#!/usr/bin/env python3

import struct
import os
from pathlib import Path
from datetime import date, timedelta
import zipfile
import time

one_week_ago = date.today() - timedelta(days=7)
demodir = Path("C:\\Program Files (x86)\\Steam\\steamapps\\common\\Team Fortress 2\\tf\\demos\\")

casual_maps = {"pl_enclosure_final", "pl_frontier_final", "pl_hoodoo_final",
               "koth_nucleus", "cp_powerhouse",
               "tr_walkway_rc2", "koth_brazil", "koth_sawmill", "cp_mercenarypark",
               "ctf_turbine", "pl_thundermountain",  "cp_dustbowl"}


# adding map name to the filename
for demofile in demodir.iterdir():
    if not demofile.suffix == ".dem":
        continue
    
    with open(demofile, "rb") as f:
        f.seek(16 + 260 + 260)
        map_name = f.read(260).decode("ascii").replace("\0", "")

    if map_name not in demofile.name:
        new_name = demofile.stem + "_" + map_name + ".dem"
        demofile.rename(demofile.parent / new_name)


for demofile in demodir.iterdir():
    if not str(demofile).endswith(".dem"):
        continue

    # setting to infinity so, if the program fails to read the
    # playback time, it defaults to not deleting
    playback_time = float("inf") 
    map_name = ""
    modification_time = date.fromtimestamp(demofile.stat().st_mtime)
    with open(demofile, "rb") as f:
        f.seek(16 + 260 + 260)
        map_name = f.read(260).decode("ascii").replace("\0", "")
        _ = f.read(260).decode("ascii").replace("\0", "")
        playback_time = struct.unpack("f", f.read(4))[0]

    if map_name in casual_maps or playback_time < 2 * 60:
        # if the demo file is a recording of a map I don't like, or if it is only of
        # under 2 minutes of gameplay delete it.
        print("deleting", round(playback_time, 2),  map_name, demofile.name)
        demofile.unlink()
    elif modification_time < one_week_ago:
        # if the demo file is a good map and old, it will be archived, and the
        # original will be deleted.
        archive_name = "D:\\archive\\" + demofile.name + ".zip"
        with zipfile.ZipFile(archive_name, mode="w") as f:
            f.write(demofile, arcname=demofile.name)
        demofile.unlink()
        print("archiving", map_name, demofile.name)
    else:
        print("ignoring", map_name, demofile.name)
        

        
        
