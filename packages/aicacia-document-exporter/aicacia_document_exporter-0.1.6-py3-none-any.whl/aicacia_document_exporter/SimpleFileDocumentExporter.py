import json
import base64
import sqlite3
from datetime import datetime

from .Document import Document, DocumentChunk, MediaType
from .DocumentExporter import DocumentExporter
from .PreprocessingModel import PreprocessingModel


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Document):
            return obj.__dict__
        elif isinstance(obj, DocumentChunk):
            return obj.__dict__
        elif isinstance(obj, MediaType):
            return obj.value
        elif isinstance(obj, bytes):
            return base64.b64encode(obj).decode('utf-8')
        else:
            return super().default(obj)


class SimpleFileDocumentExporter(DocumentExporter):
    def _create_tables(self):
        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS docs ('
            'id TEXT PRIMARY KEY, '
            'title TEXT, '
            'raw_content BLOB, '
            'content_hash INTEGER, '
            'doi TEXT, '
            'link TEXT, '
            'authors TEXT, '
            'corpus_name TEXT, '
            'sources TEXT, '
            'location TEXT, '
            'sourced_date TEXT, '
            'revision_date TEXT, '
            'provided_tags TEXT, '
            'generated_tags TEXT, '
            'metadata TEXT'
            ')'
        )

        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS chunks ('
            'doc_id TEXT, '
            'content BLOB, '
            'media_type TEXT, '
            'token_offset_position INTEGER, '
            'sequence_number INTEGER, '
            'embedding TEXT, '
            'metadata TEXT, '
            'FOREIGN KEY(doc_id) REFERENCES docs(id)'
            ')'
        )

        self.cur.execute(
            'CREATE TABLE IF NOT EXISTS refs ('
            'doc_id TEXT, '
            'reference TEXT, '
            'FOREIGN KEY(doc_id) REFERENCES docs(id)'
            ')'
        )

    def __init__(self, path, batch_size: int = 128, preprocessing_model: PreprocessingModel | None = None):
        super().__init__(batch_size, preprocessing_model)
        self.fo = open(path, "a+")
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        self._create_tables()

    @staticmethod
    def _encode_content(content: str | bytes | None):
        if content is None:
            return None
        elif isinstance(content, str):
            return content.encode('utf-16')
        elif isinstance(content, bytes):
            return content
        else:
            return json.dumps(content, cls=Encoder).encode('utf-16')

    @staticmethod
    def _encode_date(date: datetime | None):
        if date is None:
            return None
        elif isinstance(date, datetime):
            return date.isoformat()
        else:
            return json.dumps(date, cls=Encoder)

    def _flush(self, docs: list[Document]):
        for doc in docs:
            self.cur.execute(
                "INSERT INTO docs ("
                "id, title, raw_content, content_hash, doi, link, authors, corpus_name, sources, location, "
                "sourced_date, revision_date, provided_tags, generated_tags, metadata"
                ") "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    doc.id, doc.title,
                    self._encode_content(doc.raw_content), doc.content_hash,
                    doc.doi,
                    doc.link,
                    ';'.join(doc.authors),
                    doc.corpus_name,
                    ';'.join(doc.sources),
                    doc.location,
                    self._encode_date(doc.sourced_date),
                    self._encode_date(doc.revision_date),
                    ';'.join(doc.provided_tags),
                    ';'.join(doc.generated_tags),
                    json.dumps(doc.metadata, cls=Encoder)
                )
            )

            for chunk in doc.chunks:
                self.cur.execute(
                    "INSERT INTO chunks ("
                    "doc_id, content, media_type, token_offset_position, sequence_number, embedding, metadata"
                    ") "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        doc.id, self._encode_content(chunk.content), str(chunk.media_type),
                        chunk.token_offset_position, chunk.sequence_number, json.dumps(chunk.embedding, cls=Encoder),
                        json.dumps(chunk.metadata, cls=Encoder)
                    )
                )

            for reference in doc.references:
                self.cur.execute(
                    "INSERT INTO refs (doc_id, reference) VALUES (?, ?)",
                    (doc.id, reference)
                )

        self.con.commit()

    def close(self) -> None:
        self.con.close()
