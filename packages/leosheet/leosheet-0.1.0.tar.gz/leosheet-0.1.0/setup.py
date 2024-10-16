from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["shillelagh==1.1.5", "shillelagh[gsheetsapi]", "toml"]

setup(
    name="leosheet",
    version="0.1.0",
    author="Tao Xiang",
    author_email="xiang.tao@outlook.de",
    description="Python SDK for Google Sheet Interaction",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/leoxiang66/leosheet",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
