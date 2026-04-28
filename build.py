"""Build UnsplashPaper into a standalone executable."""
import platform
import subprocess
import sys

name = "UnsplashPaper"
args = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",
    "--windowed",
    "--name", name,
    "unsplashpaper.py",
]

subprocess.run(args, check=True)

ext = ".exe" if platform.system() == "Windows" else ""
print(f"\nBuild complete! Find {name}{ext} in the dist/ folder.")
