from setuptools import setup, find_packages
import os

setup(
    name='l2_data_utils',
    version= os.getenv('TAG_VERSION'),
    packages=find_packages(),
    install_requires=[
        'pyspark',
        'delta-spark',
    ],
)