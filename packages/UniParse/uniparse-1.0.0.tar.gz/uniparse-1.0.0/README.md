# UniParse

A Python library to parse PDF, DOCX, and TXT files, now with resume summarization capabilities.

## Installation

```bash
pip install UniParse
```

## How to Use
```python
from UniParse import FileParser

parser = FileParser('path/to/your/file.pdf')
content = parser.parse()
print(content)
```

## Features
- Parse text from PDF files
- Extract content from DOCX documents
- Read text from TXT files

### Parsing Resumes and Extracting Information

```python
from UniParse import ResumeParser

parser = ResumeParser('path/to/resume.pdf')
data = parser.get_extracted_data()

print("Resume Data:")
print(data)