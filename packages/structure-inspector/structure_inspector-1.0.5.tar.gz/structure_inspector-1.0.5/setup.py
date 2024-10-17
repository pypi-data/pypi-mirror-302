from setuptools import setup, find_packages

setup(
    name="structure_inspector",
    version="1.0.5",
    description="A Python package to print the structure of complex, nested Python objects.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Every AI LLC",
    author_email="opensource@everyai.llc",
    url="https://github.com/everyai/structure_inspector",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
