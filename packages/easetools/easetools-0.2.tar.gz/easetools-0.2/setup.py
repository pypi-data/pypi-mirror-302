from setuptools import setup, find_packages

setup(
    name="easetools",
    version="0.2",
    packages=find_packages(),
    install_requires=[],
    author="Y S S M Charan",
    author_email="yssmc24@gmail.com",
    description="number theory, and matrix operations. The package is designed to simplify calculations for common use cases, including arithmetic, statistical analysis, combinatorics, and linear algebra. ",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MaruthiCharan2403/easetools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)