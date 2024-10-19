from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.2'
DESCRIPTION = 'A helpfull python package!'
LONG_DESCRIPTION = 'A package that allows you to have simplicity and effectiveness in your projects!'

setup(
    name="cutepywin",
    version=VERSION,
    author="0x0060",
    author_email="<ren@0x0060.dev>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'python system Detection', 'python hex', 'python rgb', 'python hex', 'python loader', 'rich python', 'python rich', 'cutepy'],
    classifiers=[]
)
