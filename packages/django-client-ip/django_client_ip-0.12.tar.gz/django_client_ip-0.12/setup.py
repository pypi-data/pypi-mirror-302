from setuptools import setup
import os

def get_version():
    version_dict = {}
    with open(os.path.join(os.path.dirname(__file__), "__version__.py")) as f:
        exec(f.read(), version_dict)
    return version_dict['version']

setup(
    name='django-client-ip',
    version=get_version(),
    packages=['django_client_ip'],
    include_package_data=True,
    license='MIT',
    description='A Django middleware for retrieving client IP addresses and geolocation using ip-api.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Hadi Cahyadi',
    author_email='cumulus13@gmail.com',
    url='https://github.com/cumulus13/django-client-ip',  # Replace with your actual URL
    install_requires=[
        'Django>=3.0',
        'requests',
        'rich',
        ],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
)
