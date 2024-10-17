import logging
import os
import pathlib
import shutil
import uuid
from pathlib import Path
from typing import Union, List

from texta_tools.text_splitter import TextSplitter

from . import exceptions

logging.basicConfig(
	format='%(levelname)s %(asctime)s: %(message)s',
	datefmt='%d.%m.%Y %H:%M:%S',
	level=logging.INFO
)


class DocParserLite:

	def __init__(
			self,
			temp_dir: str = "",
			tika_languages: list = ["est", "eng", "rus"],
			max_file_size: int = 100,
			tika_timeout: int = 60,
			strip_text: bool = True,
			text_chunk_size: int = 3750
	):
		self.max_file_size = max_file_size
		self.temp_dir_path = pathlib.Path(temp_dir)
		self.tika_languages = tika_languages
		self.tika_timeout = tika_timeout
		self.strip_text = strip_text
		self.text_splitter = TextSplitter()
		self.text_chunk_size = text_chunk_size
		# Load Tika parser here because it loads it's ENV variables during import!
		from tika import parser
		self.parser = parser

		self.temp_dir = None

	def _create_temp_dir(self):
		"""
		Creates temp directory path.
		"""
		temp_dir = self.temp_dir_path / ("temp_" + uuid.uuid4().hex)
		if not os.path.exists(temp_dir):
			os.mkdir(temp_dir)
		return temp_dir

	def _remove_temp_dir(self):
		"""
		Removes temp directory path.
		"""
		if os.path.exists(self.temp_dir):
			shutil.rmtree(self.temp_dir)

	def _process_tika_content(self, content):
		# Replace None with empty string
		if not content:
			content = ""
		# Strip text if required
		if self.strip_text:
			lines = (line.strip() for line in content.splitlines())
			content = "\n".join(line for line in lines if line)
		# Split text into
		if self.text_chunk_size > 0:
			content = self.text_splitter.split(content, max_limit=self.text_chunk_size)
		else:
			# TODO: This is really ugly...
			content = [{"text": content, "page": 1}]
		return content

	def _parse_file(self, file_path: Path):
		"""
		Parses document using TIKA.
		"""
		tika_options = {
			"headers": {
				"X-Tika-OCRLanguage": "+".join(self.tika_languages),
				"X-Tika-PDFextractInlineImages": "true",
				"X-Tika-OCRTimeout": str(self.tika_timeout)
			},
			"timeout": self.tika_timeout
		}
		tika_output = self.parser.from_file(str(file_path), requestOptions=tika_options)
		content = tika_output["content"]
		processed_content = self._process_tika_content(content)
		return processed_content

	def _validate_file(self, file_path: Path):
		# check if file exists
		if not file_path.exists():
			raise exceptions.InvalidInputError(f"Path {file_path} does not exist.")
		# check file size
		if file_path.stat().st_size > self.max_file_size * 1024 ** 2:
			raise exceptions.InvalidInputError(f"File exceeds maximum size of {self.max_file_size} mb.")
		return True

	def _handle_paths_or_bytes(self, content: Union[str, bytes]):
		if isinstance(content, str):
			file_path = content
			return file_path

		elif isinstance(content, bytes):
			random_uuid = uuid.uuid4().hex
			file_path = self.temp_dir / random_uuid
			with open(file_path, "wb+") as fp:
				fp.write(content)
				return file_path
		else:
			raise exceptions.WrongParseInputError("Only file paths or content bytes should be given!")

	def parse(self, path_or_content: Union[str, bytes]) -> List[dict]:
		"""
		Can be eiter a path string to a file or the bytes content of a file to
		be parsed into text.
		"""

		try:
			self.temp_dir = self._create_temp_dir()

			file_path = self._handle_paths_or_bytes(path_or_content)

			# Convert to PosixPath
			file_path = Path(file_path)
			# Validate input file
			self._validate_file(file_path)
			# Create temporary directory to hold files generated during parsing.
			# Parse file
			result = self._parse_file(file_path)
			# Remove temp files
			self._remove_temp_dir()
			return result

		except Exception as e:
			self._remove_temp_dir()
			raise e


if __name__ == "__main__":
	parser = DocParserLite()
	result = parser.parse("tests/data/documents/test_pdf.pdf")
	print(result)
