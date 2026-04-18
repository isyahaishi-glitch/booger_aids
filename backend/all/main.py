import subprocess
import sys
import os

base = os.path.dirname(os.path.abspath(__file__))

processes = [
    subprocess.Popen([sys.executable, os.path.join(base, "tweet.py")]),
    subprocess.Popen([sys.executable, os.path.join(base, "rrs.py")]),
    subprocess.Popen([sys.executable, os.path.join(base, "telegram.py")]),
    subprocess.Popen([sys.executable, os.path.join(base, "plane.py")]),
]

print("All scrapers running:")
print("  tweet.py    → http://localhost:5000/tweets")
print("  rrs.py      → http://localhost:5001/antara")
print("  telegram.py → http://localhost:5002/telegram")
print("  plane.py    → http://localhost:5003/")

try:
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    print("\nStopping all scrapers...")
    for p in processes:
        p.terminate()