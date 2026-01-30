from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, FrozenSet

Value = str | int | bool | None
Field = Dict[str, Value]
FieldsDef = list[tuple[str, str]]

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
    key: str
    filename: str
    label: str
    fields: FieldsDef
    id_key: str = "id"

    int_keys: FrozenSet[str] = frozenset()
    bool_keys: FrozenSet[str] = frozenset()


FILE_DEFS: List[FileDef] = [
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


