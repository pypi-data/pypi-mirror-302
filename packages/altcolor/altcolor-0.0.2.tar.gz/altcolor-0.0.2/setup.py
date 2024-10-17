from setuptools import setup, find_packages

setup(
    name="altcolor",
    version="0.0.2",
    author="Taireru LLC",
    author_email="tairerullc@gmail.com",
    description="A package designed to add color to text in console based applications. [Credit to 'colorama' ('https://pypi.org/project/colorama/') for a few of the colors]",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TaireruLLC/altcolor",
    packages=find_packages(),
    install_requires=[
        "colorama"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
