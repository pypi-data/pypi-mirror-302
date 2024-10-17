import glob
import itertools
import os
import re
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import TypeVar
from xml.etree.ElementTree import Element

from charset_normalizer import from_path

T = TypeVar("T")


def count_trailing(source: str, chars: str) -> int:
    return len(source) - len(source.rstrip(chars))


def skip(iterable: Iterable[T], count: int) -> Iterator[T]:
    return itertools.islice(iterable, count, None)


def glob_plus(pattern: str, extension: str = "xml") -> list[Path]:
    if "*" in pattern:
        # Path.glob doesn't seem to support absolute paths
        return [Path(p) for p in glob.glob(pattern, recursive=True)]  # noqa: PTH207

    path = Path(pattern)
    if path.is_dir():
        return list(path.glob(f"**/*.{extension}"))

    return [path]


XML_ENCODING_DECLARATION = re.compile(rb'encoding="(.*?)"', re.DOTALL)


# This tries to detect the encoding from the XML declaration,
# and then reads the file with that encoding.
# This only checks for ASCII-compatible encodings, UTF-16 etc. are not supported.
def _read_text_file_fast(file_path: Path) -> str | None:
    try:
        with file_path.open("rb") as file:
            data = file.read(50)
        match = XML_ENCODING_DECLARATION.search(data)
        if match:
            # The encoding should be ASCII-compatible, since it matched the binary regex.
            enc = match.group(1).decode()
            return file_path.read_text(encoding=enc)
    except UnicodeDecodeError:
        pass

    return None


def _read_text_file_slow(file_path: Path) -> str:
    matches = from_path(file_path)
    best = matches.best()
    return str(best)


def read_text_file(file_path: Path) -> str:
    if file_path.suffix == ".xml":
        from_decl = _read_text_file_fast(file_path)
        if from_decl:
            return from_decl

    return _read_text_file_slow(file_path)


def format_xml_tag(elem: Element) -> str:
    if not elem.attrib:
        return f"<{elem.tag}>"
    attributes = " ".join(f'{name}="{value}"' for name, value in elem.attrib.items())
    return f"<{elem.tag} {attributes}>"


class AppLocalDirNotFoundError(Exception):
    """Raised when LOCALAPPDATA cannot be found."""


def get_app_local_dir() -> Path:
    local_app_data = os.getenv("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "anyerplint"
    msg = "Could not find LOCALAPPDATA"
    raise AppLocalDirNotFoundError(msg)


def add_linenumbers(cont: str, needles: list[str]) -> list[str]:
    hits: list[list[int]] = [[] for i in range(len(needles))]
    for linenum, line in enumerate(cont.splitlines(), 1):
        for _in, n in enumerate(needles):
            if n in line:
                hits[_in].append(linenum)

    return [
        n + " - line " + ", ".join(map(str, hits[idx]))
        for (idx, n) in enumerate(needles)
    ]


def _replace_with_empty(match: re.Match[str]) -> str:
    comment = match.group(0)
    return "\n" * comment.count("\n")


def replace_commented_xml_with_empty_lines(xml_string: str) -> str:
    comment_pattern = "<!--(.*?)-->"
    return re.sub(comment_pattern, _replace_with_empty, xml_string, flags=re.DOTALL)


def replace_cdata_with_empty_lines(xml_string: str) -> str:
    cdata_pattern = r"<!\[CDATA\[(.*?)\]\]>"
    return re.sub(cdata_pattern, _replace_with_empty, xml_string, flags=re.DOTALL)


XML_ENTITY_PATTERN = re.compile(r"&([^;]+);")

XML_ENTITY_MAPPINGS = {
    "lt": "<",
    "gt": ">",
    "amp": "&",
    "quot": '"',
}


def expand_xml_entities(xml_string: str) -> str:
    def replace_entity(match: re.Match[str]) -> str:
        entity = match.group(1)
        # If the entity is not in the mapping, return the original string
        return XML_ENTITY_MAPPINGS.get(entity, match.group(0))

    return XML_ENTITY_PATTERN.sub(replace_entity, xml_string)
