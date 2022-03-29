from pathlib import Path

from setuptools import (find_packages,
                        setup)

import hypothesis_sqlalchemy

project_base_url = 'https://github.com/lycantropos/hypothesis_sqlalchemy/'

setup(name='hypothesis_sqlalchemy',
      version=hypothesis_sqlalchemy.__version__,
      author='Azat Ibrakov',
      author_email='azatibrakov@gmail.com',
      url=project_base_url,
      download_url=project_base_url + 'archive/master.tar.gz',
      description=hypothesis_sqlalchemy.__doc__,
      long_description=Path('README.md').read_text(),
      long_description_content_type='text/markdown',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Framework :: Hypothesis',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Operating System :: POSIX',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Topic :: Database :: Database Engines/Servers',
      ],
      packages=find_packages(exclude=('tests', 'tests.*')),
      keywords=['SQLAlchemy', 'hypothesis'],
      python_requires='>=3.6',
      install_requires=Path('requirements.txt').read_text())
