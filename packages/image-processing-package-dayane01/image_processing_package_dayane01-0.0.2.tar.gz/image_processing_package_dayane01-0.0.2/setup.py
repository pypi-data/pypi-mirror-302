from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing_package_dayane01",
    version="0.0.2",
    author="Dayane",
    author_email="dayanepateis@gmail.com",
    description="Pacote de processamento de imagens",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DayPateis/image-processing-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5',
    )