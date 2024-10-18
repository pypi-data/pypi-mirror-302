from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='kahn_topo_sort',
    version='0.2.4',
    packages=find_packages(),
    install_requires=[
        #I think nothing
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)