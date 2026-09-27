from aether import __version__
from aether.docs.schema import Doc, DocFrontmatter


def test_version_is_exposed():
    assert __version__ == "0.1.0"


def test_document_schema_accepts_minimal_document():
    document = Doc(path=__import__("pathlib").Path("README.md"), frontmatter=DocFrontmatter(title="AETHER", slug="aether"), body="test")
    assert document.title == "AETHER"
