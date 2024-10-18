
from setuptools import setup, find_packages

setup(
    name="simon_library",
    version="0.4.0",
    packages=find_packages(),
    install_requires=[],
    author="Simon",
    author_email="bigboss@internet.com",
    description="A library for hw4",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/asm-bse/simon_library",  # Опционально
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
