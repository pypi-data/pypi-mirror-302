import os

from texta_parsers_lite.doc_parser import DocParserLite

TEST_DATA_DIR = "tests/data"

def test_file_parsing_default_settings():
    parser = DocParserLite()
    for f in os.listdir(TEST_DATA_DIR):
        f_path = os.path.join(TEST_DATA_DIR, f)
        result = parser.parse(f_path)

        assert len(result) > 0

        for item in result:
            assert "page" in item
            assert "text" in item
