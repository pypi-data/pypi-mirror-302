from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from enum import Enum


class MediaType(Enum):
    def __str__(self):
        return self.value

    TEXT = "text/plain"
    CSV = "text/csv"
    IMAGE_JPEG = "image/jpeg"


@dataclass
class DocumentChunk:
    content: str | bytes
    media_type: MediaType | str
    token_offset_position: int
    sequence_number: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    embedding: list[float] | None = None


@dataclass
class Document:
    title: str
    chunks: list[DocumentChunk]
    raw_content: str | bytes | None = None
    id: str | None = None
    authors: list[str] = field(default_factory=list)
    doi: str | None = None
    link: str | None = None
    content_hash: int | None = None
    corpus_name: str | None = None
    sources: list[str] = field(default_factory=list)
    location: str | None = None
    sourced_date: datetime | None = None
    revision_date: datetime | None = None
    provided_tags: list[str] = field(default_factory=list)
    generated_tags: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
