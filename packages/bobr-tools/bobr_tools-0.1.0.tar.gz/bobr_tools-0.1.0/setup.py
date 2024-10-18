# setup.py

from setuptools import setup, find_packages

setup(
    name="bobr_tools",
    version="0.1.0",
    packages=find_packages(),
    description="A simple package with a test function",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Artyom Bobr",
    author_email="artyombobr@gmail.com",
    url="https://github.com/yourusername/bobr_tools",  # замените на реальный URL репозитория, если он есть
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)