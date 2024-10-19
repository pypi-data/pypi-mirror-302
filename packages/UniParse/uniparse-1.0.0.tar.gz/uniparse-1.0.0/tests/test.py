from UniParse import FileParser
from resume_parser import ResumeParser

parser = FileParser('sample.pdf')
parser = ResumeParser('sample.pdf')
data = parser.get_extracted_data()

print("Resume Data:")
print(data)

