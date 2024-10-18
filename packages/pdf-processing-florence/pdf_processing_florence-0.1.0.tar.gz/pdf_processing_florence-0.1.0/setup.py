from setuptools import setup, find_packages

setup(
    name="pdf_processing_florence",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pdf2image",
        "Pillow",
        "torch",
        "transformers",
        "PyMuPDF",
    ],
    author="Carlos Rosas",
    author_email="carlos@pleias.com",
    description="A library for processing PDFs with Florence",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pdf_processing_florence",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)