from pathlib import Path
import os
import shutil
from aqt import mw


class AnkiMediaManager:
    def __init__(self, addon_name="lingoflix4anki"):
        self.addon = addon_name
        self.media_dir = Path(mw.pm.profileFolder()) / "collection.media" / self.addon
        self.addon_media_dir = Path(__file__).parent.parent.parent / addon_name


    def import_all(self):
        shutil.copytree(
            self.addon_media_dir,
            self.media_dir,
            dirs_exist_ok=True
        )

    def load_file(self, relative_path: str) -> str:
        target = self.media_dir / relative_path
        if not target.exists():
            raise FileNotFoundError(f"Could not find {target}")
        with open(target, "r", encoding="utf-8") as f:
            return f.read()

    def copy_file(self, relative_path: str):
        dest = self.media_dir / relative_path
        src = self.addon_media_dir / relative_path
        shutil.copy(src, dest)

