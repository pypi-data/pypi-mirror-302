
from setuptools import find_packages, setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='syncari-sdk',
    version='1.3.22',
    description='Syncari Synapse Development Kit',
    author='Syncari',
    author_email='dev@syncari.com',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='TBD',
    packages=find_packages(exclude=('unittests')),
    install_requires=[
        'pydantic~=1.6',
        'requests',
        'urllib3==1.26.0',
        'backoff',
        'google-cloud-logging==3.10.0'
    ],
    python_requires='>=3.7.0',
)
