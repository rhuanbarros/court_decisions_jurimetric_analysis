# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'trt4',
    version      = '1.0',
    packages     = find_packages(),
    package_data={
        'trt4': ['resources/*.csv']
    },
    entry_points = {'scrapy': ['settings = trt4.settings']},
)
