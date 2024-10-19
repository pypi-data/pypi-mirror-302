import re
import spacy
from UniParse import FileParser


try:
    nlp = spacy.load('en_core_web_sm')
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load('en_core_web_sm')

# self.nlp = nlp


class ResumeParser:
    """
    A class to parse resumes and extract structured information.
    """
    
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.text = ""
        self.data = {}
        self.nlp = nlp
    
    def extract_info(self):
        """
        Extracts text from the resume file using FileParser.
        """
        parser = FileParser(self.file_path)
        self.text = parser.parse()
        if not self.text:
            raise ValueError("Failed to extract text from the resume.")
    
    def parse(self):
        """
        Parses the resume and extracts information.
        """
        self.extract_info()
        doc = self.nlp(self.text)
        self.data['name'] = self.extract_name(doc)
        self.data['email'] = self.extract_email()
        self.data['mobile_number'] = self.extract_mobile_number()
        self.data['skills'] = self.extract_skills()
        self.data['degree'] = self.extract_degree()
        self.data['college_name'] = self.extract_college()
        self.data['total_experience'] = self.extract_experience()
        self.data['is_experienced'] = bool(self.data['total_experience'])
        self.data['no_of_pages'] = self.get_number_of_pages()
        self.data['hobbies'] = self.extract_hobbies()
    
    def extract_name(self, doc):
        """
        Extracts the name from the resume using NER.
        """
        lines = self.text.strip().split('\n')
        
        lines = [line.strip() for line in lines if line.strip()]
        
        possible_names = []
        for i in range(min(10, len(lines))):
            line = lines[i]
            for ent in doc.ents:
                if ent.label_ == 'PERSON' and len(ent.text.split()) <= 3:
                    possible_names.append(ent.text)
            
            tokens = line.split()
            capitalized_tokens = [token for token in tokens if token[0].isupper()]
            if 1 < len(capitalized_tokens) <= 3 and len(tokens) <= 5:
                possible_names.append(' '.join(capitalized_tokens))
        
        if possible_names:
            return possible_names[0]
        else:
            return None

    def extract_email(self):
        """
        Extracts email addresses using regex.
        """
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        emails = re.findall(email_pattern, self.text)
        return emails[0] if emails else None
    
    def extract_mobile_number(self):
        """
        Extracts mobile numbers using regex.
        """
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?(\d{5}[-.\s]?\d{5})'
        match = re.search(phone_pattern, self.text)
        if match:
            return match.group()
        return None
    
    def extract_skills(self):
        """
        Extracts skills from the resume.
        """
        # Define a set of skills to look for
        skills = set([
            'python', 'java', 'c++', 'machine learning', 'data analysis', 'sql', 'javascript',
            'aws', 'react', 'django', 'flask', 'docker', 'kubernetes', 'terraform', 'git',
            'pandas', 'numpy', 'matplotlib', 'fastapi', 'restful api', 'celery', 'airflow'
        ])
        extracted_skills = []
        for skill in skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', self.text, re.IGNORECASE):
                extracted_skills.append(skill)
        return extracted_skills
    
    def extract_degree(self):
        """
        Extracts degree information.
        """
        degrees = ['Bachelor', 'Master', 'B.Sc', 'M.Sc', 'B.Tech', 'M.Tech', 'PhD']
        for degree in degrees:
            if re.search(r'\b' + degree + r'\b', self.text, re.IGNORECASE):
                return degree
        return None
    
    def extract_college(self):
        """
        Extracts college or university name.
        """
        education_section = ''
        education_keywords = ['Education', 'Academic', 'Qualification', 'Educational Background', 'Education and Achievement']
        
        for keyword in education_keywords:
            pattern = rf'{keyword}.*'
            match = re.search(pattern, self.text, re.IGNORECASE | re.DOTALL)
            if match:
                education_section = self.text[match.start():]
                break

        if education_section:
            lines = education_section.split('\n')
            for line in lines:
                if 'B.Tech' in line or 'Bachelor' in line:
                    return line.strip()
        
        return None
    
    def extract_experience(self):
        """
        Extracts total experience in years from the 'Experience' section only.
        """

        from dateparser import parse
        from datetime import datetime
        import re

        date_patterns = [
            r'(?P<start_month>\w+)\s+(?P<start_year>\d{4})\s*[-–to]+\s*(?P<end_month>\w+)\s+(?P<end_year>\d{4}|present|Present)',
            r'(?P<start_month>\w+)\s+(?P<start_year>\d{4})\s*[-–to]+\s*(?P<end_year>\d{4}|present|Present)',
        ]

        experience_in_months = 0
        current_date = datetime.now()

        # Isolate the Experience section
        experience_section = self.extract_experience_section()

        employment_periods = []

        # Apply date patterns to the Experience section only
        for pattern in date_patterns:
            matches = re.finditer(pattern, experience_section, re.IGNORECASE)
            for match in matches:
                start_month = match.group('start_month')
                start_year = match.group('start_year')
                end_month = match.group('end_month') if 'end_month' in match.groupdict() else None
                end_year = match.group('end_year')

                if end_month:
                    start_date_str = f"{start_month} {start_year}"
                    end_date_str = f"{end_month} {end_year}"
                else:
                    start_date_str = f"{start_month} {start_year}"
                    end_date_str = f"{end_year}"

                start_date = parse(start_date_str)
                if end_year.lower() in ['present', 'now']:
                    end_date = current_date
                else:
                    end_date = parse(end_date_str)
                    if end_date > current_date:
                        end_date = current_date

                if start_date and end_date and start_date <= end_date:
                    employment_periods.append((start_date, end_date))

        # Remove overlaps in periods
        employment_periods = self.remove_overlaps(employment_periods)

        # Calculate total experience in months
        for start_date, end_date in employment_periods:
            months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            experience_in_months += months

        # Convert months to years
        total_experience_years = round(experience_in_months / 12, 2) if experience_in_months > 0 else None
        return total_experience_years

    def extract_experience_section(self):
        """
        Helper function to extract the 'Experience' section from the resume text.
        """
        # Define the section headers to locate 'Experience' section and ignore others
        experience_pattern = re.compile(r'(experience|work history)', re.IGNORECASE)
        education_pattern = re.compile(r'(education|academic|qualification)', re.IGNORECASE)
        project_pattern = re.compile(r'(projects|personal projects)', re.IGNORECASE)
    
        # Find the Experience section start
        experience_match = experience_pattern.search(self.text)
        if not experience_match:
            return ''  # Return empty if 'Experience' section is not found
    
        # Find the end of the Experience section by looking for next section (Education, Projects)
        start_pos = experience_match.end()
    
        # Find the next section, whichever comes first
        education_match = education_pattern.search(self.text, start_pos)
        project_match = project_pattern.search(self.text, start_pos)
    
        # Determine where the Experience section ends
        if education_match:
            end_pos = education_match.start()
        elif project_match:
            end_pos = project_match.start()
        else:
            end_pos = len(self.text)  # If no more sections, go till the end of the document
    
        # Extract only the Experience section text
        experience_section = self.text[start_pos:end_pos]
        return experience_section

    def remove_overlaps(self, periods):
        """
        Removes overlapping periods from the list of employment periods.
        """
        # Sort periods by start date
        periods.sort(key=lambda x: x[0])
        merged_periods = []
        for current_start, current_end in periods:
            if not merged_periods:
                merged_periods.append((current_start, current_end))
            else:
                last_start, last_end = merged_periods[-1]
                if current_start <= last_end:
                    # Overlapping periods, merge them
                    merged_periods[-1] = (last_start, max(last_end, current_end))
                else:
                    merged_periods.append((current_start, current_end))
        return merged_periods

    def get_number_of_pages(self):
        """
        Returns the number of pages in the resume.
        """
        # For simplicity, we'll assume one page per 500 words
        word_count = len(self.text.split())
        pages = word_count // 500 + 1
        return pages
    
    def extract_hobbies(self):
        """
        Extracts hobbies if mentioned.
        """
        hobby_pattern = r'Hobbies|Interests|Activities'
        if re.search(hobby_pattern, self.text, re.IGNORECASE):
            # Extract hobbies mentioned after the keyword
            hobbies_text = self.text.split(re.search(hobby_pattern, self.text, re.IGNORECASE).group())[-1]
            hobbies_list = hobbies_text.strip().split('\n')[0]
            return hobbies_list.strip()
        return None
    
    def get_extracted_data(self):
        """
        Returns the extracted data.
        """
        self.parse()
        return self.data