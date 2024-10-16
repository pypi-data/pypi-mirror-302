from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image-processing-robertwilliam",
    version="0.0.1",
    author="Robert William",
    author_email="rw.codemaster@outlook.com",
    description="Teste Pypi",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DevRobertW/simple-package-template",
    packages=find_packages(),
    install_requires=requirements,
    
)