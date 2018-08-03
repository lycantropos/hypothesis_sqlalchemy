from setuptools import (setup,
                        find_packages)

import hypothesis_sqlalchemy
from hypothesis_sqlalchemy.config import PROJECT_NAME

project_base_url = 'https://github.com/lycantropos/hypothesis_sqlalchemy/'

install_requires = [
    'sqlalchemy>=1.1.14',
    'hypothesis>=3.28.0',
]
setup_requires = [
    'pytest-runner>=2.11',
]
tests_require = [
    'pydevd>=1.0.0',  # debugging
    'sqlalchemy_helpers>=0.1.0',  # context managers
    'sqlalchemy_utils>=0.32.16',  # database creation/destruction
    'pytest>=3.0.5',
    'pytest-cov>=2.4.0',
    'hypothesis>=3.13.0',
]

setup(name=PROJECT_NAME,
      version=hypothesis_sqlalchemy.__version__,
      author='Azat Ibrakov',
      author_email='azatibrakov@gmail.com',
      url=project_base_url,
      download_url=project_base_url + 'archive/master.tar.gz',
      description=hypothesis_sqlalchemy.__doc__,
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Operating System :: POSIX',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Topic :: Database :: Database Engines/Servers',
      ],
      packages=find_packages(exclude=('tests',)),
      keywords=['SQLAlchemy', 'hypothesis'],
      python_requires='>=3.5',
      install_requires=install_requires,
      setup_requires=setup_requires,
      tests_require=tests_require)
