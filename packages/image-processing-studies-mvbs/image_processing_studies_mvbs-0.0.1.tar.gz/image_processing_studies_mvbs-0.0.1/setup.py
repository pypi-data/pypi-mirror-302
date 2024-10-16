from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "image_processing_studies_mvbs",
    version = "0.0.1",
    author= "Karina, and student Marcelo",
    description = "image processing package using skimage to study",
    long_description = page_description,
    url = "https://github.com/mvbs3/image-processing-package",
    packages = find_packages(),
    install_requires = requirements,
    python_requires = '>=3.5',
)