from setuptools import setup, find_packages

setup(
    name="hamidreza",
    version="0.3",
    description="personal info about Hamidreza",
    author="Hamidreza",
    author_email="h4midrezam@gmail.com",
    packages=find_packages(include=["hamidreza", "hamidreza.*"]),
    install_requires=[],
)
