from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="diffpatrol",
    version="0.1.0",
    author="Mark Lechner",
    author_email="lechner.mark@gmail.com",
    description="DiffPatrol is a Python tool for analyzing project dependencies through various means such as diffs, commit history, and CI/CD logs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/diffpatrol",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "diffpatrol=diffpatrol.cli:main",
        ],
    },
)
