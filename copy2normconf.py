from shutil import copy
from pathlib import Path

normconf_folder = Path("../website/")

assert normconf_folder.exists(), "Normconf Folder doesn't exist"

paths = Path("data/").glob("**/*.html")

(normconf_folder / "transcripts").mkdir(exist_ok=True)

for p in paths:
    name = p.parent.parent.stem
    copy(p, normconf_folder / "transcripts" / f"{name}.html")