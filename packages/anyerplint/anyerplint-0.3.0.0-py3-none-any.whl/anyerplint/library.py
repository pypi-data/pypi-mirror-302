import zipfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import IO


@dataclass
class Library:
    """Stores known symbols from the 'standard library'."""

    variables: set[str]
    loopvariables: set[str]
    calls: set[str]
    jumps: set[str]
    tags: set[str]
    # if true, accumulate everything found to library
    teaching: bool

    def _visit_file(self, fname: str, fobj: IO[bytes]) -> None:
        def feed_set(dest: set[str], fobj: IO[bytes]) -> None:
            dest.update(line.decode().strip() for line in fobj.readlines())

        if fname.endswith("_calls.txt"):
            feed_set(self.calls, fobj)
        elif fname.endswith("_jumps.txt"):
            feed_set(self.jumps, fobj)
        elif fname.endswith("_tags.txt"):
            feed_set(self.tags, fobj)
        elif fname.endswith("_vars.txt"):
            feed_set(self.variables, fobj)
        elif fname.endswith("_loopvars.txt"):
            feed_set(self.loopvariables, fobj)
            self.loopvariables = {lv.lower() for lv in self.loopvariables}

    def load_from_disk(self, libdir: Path) -> None:
        """Load the library from disk. Can be called multiple times."""
        if not libdir.exists():
            return

        # files on file system
        for p in libdir.glob("*_*.txt"):
            self._visit_file(str(p), p.open("rb"))

        # files in all the zip files
        for f in libdir.glob("*.zip"):
            zf = zipfile.ZipFile(f, "r")
            for zn in zf.namelist():
                self._visit_file(zn, zf.open(zn, "r"))

    def save_to_disk(self, target_path: Path, emit: Callable[[str], None]) -> None:
        """Save the library to disk."""

        def write_file(fname: Path, lines: list[str]) -> None:
            emit(f"  - {fname}")
            with fname.open("wb") as f:
                for line in lines:
                    try:
                        if not line.strip().isascii():
                            continue
                        enc = line.strip().encode()
                    except UnicodeEncodeError:
                        # skip bad lines for now
                        continue
                    f.write(enc)
                    f.write(b"\n")

        emit("Writing found function to:")

        calls_file = target_path / "builtin_calls.txt"
        write_file(calls_file, sorted(self.calls))

        jumps_file = target_path / "builtin_jumps.txt"
        write_file(jumps_file, sorted(self.jumps))

        tags_file = target_path / "builtin_tags.txt"
        write_file(tags_file, sorted(self.tags))

        vars_file = target_path / "builtin_vars.txt"
        write_file(vars_file, sorted(self.variables))

        loopvars_file = target_path / "builtin_loopvars.txt"
        write_file(loopvars_file, sorted({lv.lower() for lv in self.loopvariables}))
