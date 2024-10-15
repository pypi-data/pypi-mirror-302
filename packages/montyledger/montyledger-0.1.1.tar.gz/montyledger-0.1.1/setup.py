# setup.py
from setuptools import setup, find_packages

setup(
    name='montyledger',
    version='0.1.1',
    description='monty client',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='MontyGovernance',
    author_email='eugene.and.monty@gmail.com',
    packages=find_packages(),
    install_requires=['orjson', 'xxhash', 'asyncio', 'typing'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
