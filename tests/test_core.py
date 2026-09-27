from aether import __version__
from aether.docs.schema import Document


def test_version_is_exposed():
    assert __version__ == "0.1.0"


def test_document_schema_accepts_minimal_document():
    document = Document(title="AETHER", content="test")
    assert document.title == "AETHER"
