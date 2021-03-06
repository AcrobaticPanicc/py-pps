from setuptools import setup, find_packages
from io import open
from os import path
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# automatically captured required modules for install_requires in requirements.txt
with open(path.join(HERE, './requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' not in x]


setup(
    name='py-pps',
    description='A beautiful alternative for the "docker ps" command',
    version='1.0.3',
    packages=find_packages(),
    install_requires=['setuptools~=60.2.0',
                      'rich~=12.4.1',
                      'docker~=5.0.3'],
    scripts=['pypps/app.py', 'pypps/run.py'],
    entry_points={
        'console_scripts': [
            'pps=run:main'
        ]
    },
    author="Tomer Chaim",
    keyword="docker, docker ps, cli",
    long_description=README,
    long_description_content_type="text/markdown",
    license='MIT',
    py_modules=['pypps', 'docker', 'rich'],
    url='https://github.com/AcrobaticPanicc/py-pps',
    dependency_links=dependency_links,
    author_email='chaim.tomer@gmail.com',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
