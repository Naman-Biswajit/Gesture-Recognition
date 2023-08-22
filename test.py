import subprocess, sys

opener = "open" if sys.platform == "darwin" else "xdg-open"
subprocess.call([opener, "./data/1.jpg"])