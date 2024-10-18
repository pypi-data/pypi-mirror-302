import ckonlpy
import setuptools
from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="ats_ckonlpy",
    # version=ckonlpy.__version__,
    # author=ckonlpy.__author__,
    version='1.0.1',
    author='csu5216',
    author_email='csu5216@gmail.com',
    description="KoNLPy wrapping package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/whfh3900/ats_ckonlpy.git',
    packages=setuptools.find_packages(),
    package_data={
        'ckonlpy':['data/*/*.txt', 'data/*/*/*.txt', 'data/templates/*']
    },
    install_requires=["Jpype1>=0.6.1", "konlpy>=0.4.4"],
    classifiers=(
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
)
