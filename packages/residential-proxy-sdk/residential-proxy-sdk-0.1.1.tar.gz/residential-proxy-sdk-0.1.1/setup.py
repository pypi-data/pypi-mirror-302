from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="residential-proxy-sdk",
    version="0.1.1",
    description="A proxy SDK for managing rotating residential proxies in Vietnam",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ghant Hoang",
    author_email="thaithang115@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
