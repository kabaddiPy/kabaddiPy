# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ProKabaddi_API",
    version="0.1.0",
    author="Aniruddha Mukherjee",
    author_email="mukh.aniruddha@gmail.com",
    description="A Python module for aggregating Kabaddi data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/annimukherjee/ProKabaddi_API",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "selenium",
        "pandas",
        # Add any other dependencies here
    ],
)
