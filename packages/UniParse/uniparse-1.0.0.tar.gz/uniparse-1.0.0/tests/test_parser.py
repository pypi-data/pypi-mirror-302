import os
import unittest
from UniParse import FileParser

class TestFileParser(unittest.TestCase):
    def setUp(self):
        self.current_dir = os.path.dirname(__file__)
        self.txt_file = os.path.join(self.current_dir, 'sample.txt')
        self.pdf_file = os.path.join(self.current_dir, 'sample.pdf')
        self.docx_file = os.path.join(self.current_dir, 'sample.docx')

    def test_txt_parser(self):
        parser = FileParser(self.txt_file)
        content = parser.parse()
        self.assertIsNotNone(content)

    def test_pdf_parser(self):
        parser = FileParser(self.pdf_file)
        content = parser.parse()
        self.assertIsNotNone(content)

    def test_docx_parser(self):
        parser = FileParser(self.docx_file)
        content = parser.parse()
        self.assertIsNotNone(content)

if __name__ == '__main__':
    unittest.main()