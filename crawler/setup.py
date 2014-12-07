import os
from setuptools import setup, find_packages

setup(
    name = "PriceWatcher",
    version = "0.1",
    packages = find_packages('src'),
    package_dir = {'':'src'},
    scripts = [],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = [],
    package_data = {},
    entry_points={
        'console_scripts': [
            'pw-run-crawlers=pricewatcher.scripts.run_crawlers:run',
            'pw-run-parsers=pricewatcher.scripts.run_parsers:run',
            #'bar = other_module:some_func',
        ],        
    },
    # metadata for upload to PyPI
    author = "Kevin Cheng",
    author_email = "",
    description = "",
    license = "",    
)