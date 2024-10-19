import os
from typing import Optional
import fitz
from docx import Document
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FileParser:
    SUPPOERTED_TYPES = ('.pdf', '.docx', '.txt')
    
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.file_type = self._determine_file_type()
        self.content: Optional[str] = None
    
    def _determine_file_type(self) -> str:
        _, ext = os.path.splitext(self.file_path.lower())
        if ext in self.SUPPOERTED_TYPES:
            return ext[1:]
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    def parse(self) -> Optional[str]:
        parser_method = getattr(self, f'_parse_{self.file_type}', None)
        if not parser_method:
            raise NotImplementedError(f"Parser for {self.file_type} files is not implemented")
        
        try:
            self.content = parser_method()
            logger.info(f"Successfully parsed {self.file_path}")
            return self.content
        except Exception as e:
            logger.error(f"Error parsing {self.file_path}: {e}")
            return None
    
    def _parse_pdf(self) -> str:
        text = []
        try:
            with fitz.open(self.file_path) as doc:
                for page_num, page in enumerate(doc, start=1):
                    page_text = page.get_text()
                    text.append(page_text)
                    if page_num % 10 == 0:
                        logger.debug(f"Parsed {page_num} pages.")
            return '\n'.join(text)
        except Exception as e:
            logger.exception("Failed to parse PDF.")
            raise RuntimeError(f"Failed to parse PDF: {e}")
    
    def _parse_docx(self) -> str:
        try:
            doc = Document(self.file_path)
            full_text = [para.text for para in doc.paragraphs]
            return '\n'.join(full_text)
        except Exception as e:
            logger.exception("Failed to parse DOCX.")
            raise RuntimeError(f"Failed to parse DOCX: {e}")
    
    def _parse_txt(self) -> str:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                with open(self.file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                logger.exception("Failed to parse TXT with alternative encoding.")
                raise RuntimeError(f"Failed to parse TXT: {e}")
        except Exception as e:
            logger.exception("Failed to parse TXT.")
            raise RuntimeError(f"Failed to parse TXT: {e}")