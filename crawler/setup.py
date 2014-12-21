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
    install_requires = ['Beautifulsoup4', 'elasticsearch'],
    package_data = {},
    entry_points={
        'console_scripts': [
            'pw-run-crawlers=pricewatcher.scripts.run_crawlers:run',
            'pw-run-parsers=pricewatcher.scripts.run_parsers:run',
            # Logging and Status
            'monitor-log-rotation=pricewatcher.scripts.log_rotation:run',
            'monitor-crawler-report=pricewatcher.scripts.crawler_report:run',            
        ],        
    },
    # metadata for upload to PyPI
    author = "",
    author_email = "",
    description = "",
    license = "",    
)
