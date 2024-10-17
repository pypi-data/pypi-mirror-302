from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="pacote-hello-world",
    version="0.0.1",
    author="Emanuel Saimon",
    author_email="esaimon149@gmail.com",
    description="Print hello world in different languages",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EmanuelSaimon/pacote-hello-world",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)