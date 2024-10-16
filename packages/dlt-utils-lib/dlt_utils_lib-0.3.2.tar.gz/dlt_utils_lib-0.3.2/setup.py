from setuptools import setup, find_packages

setup(
    name='dlt_utils_lib',
    version='0.3.2',
    packages=find_packages(),
    install_requires=[
        'pyspark',
        'delta-spark'
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
)