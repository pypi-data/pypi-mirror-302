import re
import nltk
from .parser import FileParser


try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt_tab', quiet=True)
    nltk.download('stopwords', quiet=True)

class ResumeSummary:
    """
    A class to extract and summarize text from resumes.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.text = ""
        self.summary = ""

    def extract_text(self):
        """
        Extracts text from the resume file using FileParser.
        """
        parser = FileParser(self.file_path)
        self.text = parser.parse()
        if not self.text:
            raise ValueError("Failed to extract text from the resume.")

    def preprocess_text(self):
        """
        Preprocesses the extracted text for summarization.
        """
        # Remove non-ASCII characters
        text = self.text.encode('ascii', 'ignore').decode()
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        self.text = text

    def summarize(self, n=5):
        """
        Summarizes the preprocessed text into n sentences.
        """
        from nltk.tokenize import sent_tokenize, word_tokenize
        from nltk.corpus import stopwords
        from string import punctuation

        stop_words = set(stopwords.words('english') + list(punctuation))
        words = word_tokenize(self.text)

        # Calculate word frequencies
        freq = {}
        for word in words:
            if word not in stop_words:
                freq[word] = freq.get(word, 0) + 1

        # Normalize frequencies
        max_freq = max(freq.values()) if freq else 1
        for word in freq.keys():
            freq[word] = freq[word] / max_freq

        # Score sentences
        sentences = sent_tokenize(self.text)
        sentence_scores = {}
        for sentence in sentences:
            sentence_words = word_tokenize(sentence.lower())
            for word in sentence_words:
                if word in freq:
                    sentence_scores[sentence] = sentence_scores.get(sentence, 0) + freq[word]

        # Select top n sentences
        summarized_sentences = sorted(
            sentence_scores, key=sentence_scores.get, reverse=True
        )[:n]
        self.summary = ' '.join(summarized_sentences)

    def get_summary(self, n=5):
        """
        Executes the full pipeline to extract and summarize the resume text.
        """
        self.extract_text()
        self.preprocess_text()
        self.summarize(n=n)
        return self.summary