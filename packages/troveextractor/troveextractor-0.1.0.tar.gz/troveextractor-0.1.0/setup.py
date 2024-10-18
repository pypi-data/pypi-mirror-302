from setuptools import setup, find_packages

setup(
    name='troveextractor',
    version='0.1.0',
    description='A simple library to return greeting messages.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
