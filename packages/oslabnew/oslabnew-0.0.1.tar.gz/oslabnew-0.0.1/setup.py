from setuptools import setup, find_packages

setup(
    name="oslabnew",
    version="0.0.1",
    description="A Python library with various useful OS code snippets.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="mdimado",
    author_email="mdimad005@gmail.com",
    url="https://github.com/mdimado/oslabnew",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
