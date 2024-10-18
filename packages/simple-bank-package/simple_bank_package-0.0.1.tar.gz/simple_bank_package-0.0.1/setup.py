from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="simple-bank-package",
    version="0.0.1",
    author="Rafael Alves",
    author_email="rvf_alves@yahoo.com.br",
    description="Simple functions for bank operation",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rvfalves/simple-package-template",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)