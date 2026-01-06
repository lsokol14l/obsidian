from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="obsidian-vault",
    version="0.1.0",
    author="Obsidian Integration",
    description="A Python library for working with Obsidian vaults",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lsokol14l/obsidian",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pyyaml>=5.4.0",
    ],
)
