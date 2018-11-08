from setuptools import find_packages, setup

setup(
    name='datagovuk',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/drewsonne/datagovuk',
    license='LGPLv3',
    author='Drew J. Sonne',
    author_email='drew.sonne@gmail.com',
    description='Tool to allow easy importing to data from data.gov.uk',
    install_requires=[
        'ckanapi', 'ruamel.yaml', 'anytree',
        'pandas', 'pyarrow'
    ],
)
