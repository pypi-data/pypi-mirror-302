from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Pre_processamento",
    version="0.0.1",
    author="Alexsandro Da Silva Bezerra",
    author_email="alecsbezerra@gmail.com",
    description="Pré-processamento de corpus para português e inglês usando spaCy.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexxs2/Pr--processamento.pacote",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)