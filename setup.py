from setuptools import setup, find_packages

setup(
    name="private_search_set",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flor",
        "click",
    ],
    entry_points='''
        [console_scripts]
        private-search-set=private_search_set.cli:main
    ''',
)