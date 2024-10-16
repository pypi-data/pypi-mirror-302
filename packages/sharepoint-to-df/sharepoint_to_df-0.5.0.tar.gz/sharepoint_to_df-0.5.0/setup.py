from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of your README file
README = Path('README.md').read_text()

setup(
    name='sharepoint_to_df',
    version='0.5.0',  # Update the version number
    description='A library to fetch SharePoint list data and return it as a Pandas DataFrame.',
    long_description=README,  # Include the content of README.md
    long_description_content_type='text/markdown',  # Indicate that the README is in Markdown format
    author='Mutaz Younes',
    author_email='mutazyounes@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'office365-rest-python-client'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
