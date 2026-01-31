from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, FrozenSet

Value = str | int | bool | None
Field = Dict[str, Value]
FieldsDef = list[tuple[str, str]]

BOOK_FIELDS: FieldsDef = [
    ("firstName", "First Name"),
    ("lastName", "Last Name"),
    ("title", "Title"),
    ("originalTitle", "Original Title"),
    ("worldHero", "World / Character"),
    ("numberInSeries", "Book in Series"),
    ("subSeries", "Cycle"),
    ("numberInSubSeries", "Book in Cycle"),
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
    key: str
    filename: str
    label: str
    fields: FieldsDef
    id_key: str = "id"

    int_keys: FrozenSet[str] = frozenset()
    bool_keys: FrozenSet[str] = frozenset()


FILE_DEFS: list[FileDef] = [
    FileDef(
        key="books",
        filename="books.json",
        label="Books",
        fields=BOOK_FIELDS,
        int_keys=frozenset({"numberInSeries", "numberInSubSeries"}),
    ),
    FileDef(
        key="lego",
        filename="lego.json",
        label="LEGO",
        fields=LEGO_FIELDS,
        int_keys=frozenset({"year", "number"}),
    ),
    FileDef(
        key="paperModels",
        filename="paperModels.json",
        label="Paper Models",
        fields=MM_FIELDS,
        int_keys=frozenset({"year", "number", "scale"}),
        bool_keys=frozenset({"owned"}),
    ),
    FileDef(
        key="wasgij",
        filename="wasgij.json",
        label="Wasgij",
        fields=WASGIJ_FIELDS,
        int_keys=frozenset({"numberInSeries", "pieces", "piecesInBox"}),
        bool_keys=frozenset({"owned"}),
    ),
]


