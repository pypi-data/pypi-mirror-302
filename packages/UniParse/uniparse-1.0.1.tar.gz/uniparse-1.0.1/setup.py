import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UniParse",
    version="1.0.1",
    author="Hridesh",
    keywords='parse parser pdf docx txt uniparse uniparser',
    author_email="hridesh.khandal@gmail.com",
    description="A library to parse PDF, DOCX, and TXT files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hridesh-net/praserlib.git",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
    ],
    python_requires='>=3.8',
    install_requires=[
        "PyMuPDF>=1.18.0",
        "python-docx>=0.8.10",
        "nltk>=3.5",
        "spacy>=3.0.0",
        "dateparser>=1.2.0",
    ]
)