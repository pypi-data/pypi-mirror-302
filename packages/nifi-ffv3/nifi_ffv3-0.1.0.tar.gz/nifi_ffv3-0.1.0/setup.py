
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nifi_ffv3",
    version="0.1.0",
    author="Alfredo Prates - Larn or Die",
    author_email="qwer.alfredo@gmail.com",
    description="Python library to manipulate the flowfile-v3 format used by Apache NiFi.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qweralfredo/nifi_ffv3.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires='>=3.6',
)