# setup.py

from setuptools import setup, find_packages

setup(
    name='onefiler',
    version='0.0.1',
    author='Fabio Pipitone',
    author_email='fabio.pipitone93@gmail.com',
    description='A tool to create a unique file with contents of other files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/fabiopipitone/onefiler',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'onefiler=onefiler.main:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ]
)
