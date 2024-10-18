from setuptools import setup, find_packages

setup(
    name="daleel",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A minimal PyPI project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/daleel",  # optional if hosted on GitHub
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
