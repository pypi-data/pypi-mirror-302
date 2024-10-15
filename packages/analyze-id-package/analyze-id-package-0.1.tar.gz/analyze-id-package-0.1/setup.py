from setuptools import setup, find_packages

setup(
    name="analyze-id-package",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "boto3",
    ],
    description="A Python package to analyze identity documents using AWS Textract's AnalyzeID feature.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Swarup Adhikary",
    author_email="swarup.ogma@example.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)