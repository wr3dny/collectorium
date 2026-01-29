from typing import Dict

Value = str | int | None
Field = Dict[str, Value]

BOOK_FIELDS: list[tuple[str, str]] = [
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


WASGIJ_FIELDS: list[tuple[str, str]] = [
    ("title", "Title"),
    ("publisher", "Publisher"),
    ("series", "Series"),
    ("numberInSeries", "Number in Series"),
    ("pieces", "Pieces"),
    ("piecesInBox", "Pieces in Box"),
    ("owned", "Owned"),
]

MM_FIELDS: list[tuple[str, str]] = [
    ("title", "Title"),
    ("year", "Year"),
    ("number", "Number"),
    ("scale", "Scale"),
    ("owned", "Owned"),
]

LEGO_FIELDS: list[tuple[str, str]] = [
    ("title", "Title"),
    ("year", "Year"),
    ("number", "Number"),
    ("series", "Series"),
]

