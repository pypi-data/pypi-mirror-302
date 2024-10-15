# setup.py
from setuptools import setup, find_packages

setup(
    name="mlszsixsixsix",
    version="0.1",
    author="牛文豪",
    author_email="your-email@example.com",
    description="A demo package for testing purposes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-github/mlszsixsixsix",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pillow"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
