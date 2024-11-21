from setuptools import setup, find_packages


def read_requirements():
    with open('requirements.txt') as f:
        return [line.strip() for line in f.readlines()]


setup(
    name="PyAPI",
    version="0.0.1",
    packages=find_packages(),
    install_requires=read_requirements(),
    author="ofri rom",
    description="Python SDK for API with queue over redis pubsub",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
