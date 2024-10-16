import re
import datetime

from simhash import Simhash
from langchain_huggingface import HuggingFaceEmbeddings

from aicacia_document_exporter.Document import Document, DocumentChunk, MediaType
from aicacia_document_exporter.SimpleFileDocumentExporter import SimpleFileDocumentExporter
from aicacia_document_exporter.PreprocessingModel import PreprocessingModel


class Preprocess(PreprocessingModel):
    def __init__(self):
        self.model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': False}
        )

    def preprocess_batch(self, docs: list[Document]):
        chunks = [chunk for doc in docs for chunk in doc.chunks]
        text_chunks = [chunk for chunk in chunks if chunk.media_type == MediaType.TEXT]
        embeddings = self.model.embed_documents([chunk.content for chunk in text_chunks])

        for i, chunk in enumerate(text_chunks):
            chunk.embedding = embeddings[i]

        for doc in docs:
            if isinstance(doc.raw_content, str):
                doc.content_hash = self.make_simhash(doc.raw_content)

    def make_simhash(self, s):
        return Simhash(self.make_features(s)).value

    @staticmethod
    def make_features(s):
        width = 3
        s = s.lower()
        s = re.sub(r'\W+', '', s)
        return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]


if __name__ == '__main__':
    with SimpleFileDocumentExporter("test.db", batch_size=32, preprocessing_model=Preprocess()) as exporter:
        ids = exporter.insert([
            Document(
                title="Title 1",
                chunks=[
                    DocumentChunk("Hello", MediaType.TEXT, 0, metadata={"semantic_position": "Abstract"}),
                    DocumentChunk(b"Image", MediaType.IMAGE_JPEG, 100)
                ],
                raw_content="Hello!!!",
                doi='1235',
                references=['Author 1', 'Author 2'],
                metadata={
                    'h1': '123'
                }
            ),
            Document(
                title="Title 2",
                chunks=[],
                revision_date=datetime.datetime.now(),
                doi="7890",
                link="link!111"
            )
        ])

        assert len(ids) == 2
