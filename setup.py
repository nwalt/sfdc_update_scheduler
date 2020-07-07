#1/usr/bin/python3
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

NAME = 'sfdc_update_scheduler'
DESCRIPTION = 'Scheduled updates for a salesforce environment, through the bulk api'
LONG_DESCRIPTION = (here / 'README.md').read_text(encoding='utf-8')
URL = 'https://github.com/nwalt/sfdc_update_scheduler'
EMAIL = 'nathanhwalton@gmail.com'
AUTHOR = 'Nathan Walton'
REQUIRES_PYTHON = '>=3.6.0' #uses f-strings
VERSION = '1.0.0'

REQUIRED = [
    'simple_salesforce'
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    py_modules=['sfdc_update_scheduler'],
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    entry_points={'console_scripts':[
        'sfdc_update_scheduler = sfdc_update_scheduler:main'
    ]}
)