from setuptools import setup, find_packages

setup(
    name="IkonGlobals",
    version="0.1",
    packages=find_packages(),
    description="A package to hold all of the data structures and functions common to other ikon repos",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Samuel Sallee",
    author_email="samsallee16@gmail.com",
    url="https://github.com/IkonAI-App/IkonGlobals",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        "pynamodb>=6.0.0",
        "pynamodb-attributes>=0.5.0",
        "pytz>=2022.7.1",
        "boto3>=1.34.82",
        "pycountry>=24.6.1",
        "opensearch-py>=2.6.0",
        "sentry-sdk>=2.16.0",
        "Werkzeug>=3.0.4",

    ],
)
