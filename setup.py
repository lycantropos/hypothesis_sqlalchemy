from pathlib import Path

from setuptools import (find_packages,
                        setup)

import hypothesis_sqlalchemy

project_base_url = 'https://github.com/lycantropos/hypothesis_sqlalchemy/'

setup(name=hypothesis_sqlalchemy.__name__,
      packages=find_packages(exclude=('tests', 'tests.*')),
      version=hypothesis_sqlalchemy.__version__,
      description=hypothesis_sqlalchemy.__doc__,
      long_description=Path('README.md').read_text(encoding='utf-8'),
      long_description_content_type='text/markdown',
      author='Azat Ibrakov',
      author_email='azatibrakov@gmail.com',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Web Environment',
          'Framework :: Hypothesis',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Operating System :: POSIX',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Topic :: Database :: Database Engines/Servers',
      ],
      keywords=['SQLAlchemy', 'hypothesis'],
      license='MIT License',
      url=project_base_url,
      download_url=project_base_url + 'archive/master.zip',
      python_requires='>=3.6',
      install_requires=Path('requirements.txt').read_text(encoding='utf-8'))
