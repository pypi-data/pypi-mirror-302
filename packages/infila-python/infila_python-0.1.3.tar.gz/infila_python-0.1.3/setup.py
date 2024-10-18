from setuptools import setup, find_packages

setup(
    name='infila-python',
    version='0.1.3',
    author='whysisisis',
    author_email='whysisisis@gmail.com',
    description='A library for file information and manipulation',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)