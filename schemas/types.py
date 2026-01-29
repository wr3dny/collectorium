from __future__ import annotations

from dataclasses import dataclass
from typing import Dict , List , Union , Tuple

Value = Union[str, int,  bool, None]
Field = Dict[str, Value]
FieldsDef = List[Tuple[str, str]]

BOOK_FIELDS: FieldsDef = [
    ("author", "Author"),
    ("title", "Title"),
    ("originalTitle", "Original Title"),
    ("worldHero", "World / Character"),
    ("numberInSeries", "Number in Series"),
    ("subSeries", "Sub-Series"),
    ("numberInSubSeries", "Number in Sub-Series"),
    ("format", "Format"),
    ("language", "Language"),
]


WASGIJ_FIELDS: FieldsDef = [
    ("title", "Title"),
    ("publisher", "Publisher"),
    ("series", "Series"),
    ("numberInSeries", "Number in Series"),
    ("pieces", "Pieces"),
    ("piecesInBox", "Pieces in Box"),
    ("owned", "Owned"),
]

MM_FIELDS: FieldsDef = [
    ("title", "Title"),
    ("year", "Year"),
    ("number", "Number"),
    ("scale", "Scale"),
    ("owned", "Owned"),
]

LEGO_FIELDS: FieldsDef = [
    ("title", "Title"),
    ("year", "Year"),
    ("number", "Number"),
    ("series", "Series"),
]


@dataclass(frozen=True)
class FileDef:
    """
    Registry entry for one JSON collection file.
    Add a new file here and the menu + loading will work automatically.
    """
    key: str                 # internal identifier (stable)
    filename: str            # file on disk (in files/ dir)
    label: str               # menu display name
    fields: FieldsDef        # which fields are relevant for this file
    id_key: str = "id"       # which key should be coerced/sorted as an integer


FILE_DEFS: List[FileDef] = [
    FileDef(key="books",       filename="books.json",       label="Books",       fields=BOOK_FIELDS),
    FileDef(key="lego",        filename="lego.json",        label="LEGO",        fields=LEGO_FIELDS),
    FileDef(key="paperModels", filename="paperModels.json", label="Paper Models", fields=MM_FIELDS),
    FileDef(key="wasgij",      filename="wasgij.json",      label="Wasgij",      fields=WASGIJ_FIELDS),
]

