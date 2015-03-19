# Dummy egg used for testing
from setuptools import setup, find_packages

version = '1.0.0'

deps = [
    'Flask-Mail==0.9.0',
    'Flask-Migrate',
    'Flask-RESTful==0.2.11',
    'Flask-SQLAlchemy==1.0',
    'Flask-Script==0.6.3',
    'Flask-WTF==0.9.3',
    'Flask==0.10.1',

    'psycopg2',
    'coverage==3.7',
    'nose==1.3.0',

    'Fabric',
    'fabtools',

    'lxml',
    'setuptools',
    'six',
    'uWSGI==1.9.21.1',
    'celery',
    'redis',
    'requests',
    'pyquery'
]

setup(name='cwr',
      version=version,
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=deps,
)
