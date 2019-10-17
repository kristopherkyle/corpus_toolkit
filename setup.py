import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="corpus_toolkit",
    version="0.27",
    author="Kristopher Kyle",
    author_email="kristopherkyle1@gmail.com",
    description="A simple Python toolkit for corpus analyses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://kristopherkyle.github.io/corpus_toolkit/",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)