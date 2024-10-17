from setuptools import setup, find_packages

setup(
    name="RacoGPT",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Francesco",
    author_email="francesco.raco@live.it",
    description="Python client library for function calling interactions with Ollama REST API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FrancescoRaco/RacoGPT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)