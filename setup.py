import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="corpus_toolkit",
    version="0.05",
    author="Kristopher Kyle",
    author_email="kristopherkyle1@gmail.com",
    description="A simple Python toolkit for corpus analyses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kristopherkyle/corpus_toolkit/tree/master/corpus_toolkit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)