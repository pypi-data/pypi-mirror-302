import __main__
import asyncio
import dolce.realtime
import dolce.writer
import dolce.reader
from datetime import datetime
from .utils import *
from .version import *


try:
    from __main__ import __file__ # running a python script.py?
    _SCRIPT = True
except ImportError: # running from shell
    _SCRIPT = False


def proc(events, path="", ask=False):
    """Processes every thing!
    Set ask to True to listen first and decide to write 
    to the disk or not afterwards."""
    print(f"Dolce v{version}")
    if path: # write to a midi file
        writer.save(events, path)
        print(f"Saved {path} at {datetime.now()}")
    else: # play now
        if ask:
            asyncio.run(realtime.play(events, _SCRIPT))
            mid_path = input("Spec path ( without suffix ) to save\n")
            if mid_path:
                writer.save(events, mid_path + ".mid")
                print(f"Wrote to {mid_path}.mid at {datetime.now()}")
        else:
            asyncio.run(realtime.play(events, _SCRIPT))
