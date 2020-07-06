from setuptools import setup, find_packages

NAME = 'sfdc_update_scheduler'
DESCRIPTION = 'Scheduled updates for a salesforce environment, through the bulk api'
URL = 'https://github.com/nwalt/sfdc_update_scheduler'
EMAIL = 'nathanhwalton@gmail.com'
AUTHOR = 'Nathan Walton'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '1.0.0'

REQUIRED = [
    'simple_salesforce'
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    py_modules=['sfdc_update_scheduler'],
    install_requires=REQUIRED,
    entry_points={'console_scripts':[
        'sfdc_update_scheduler = sfdc_update_scheduler:main'
    ]}
)