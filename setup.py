from setuptools import (find_packages,
                        setup)

import hypothesis_sqlalchemy

project_base_url = 'https://github.com/lycantropos/hypothesis_sqlalchemy/'

install_requires = [
    'sqlalchemy>=1.1.0',
    'hypothesis>=3.20.0',
]
setup_requires = [
    'pytest-runner>=4.2',
]
tests_require = [
    'pytest>=3.8.1',
    'pytest-cov>=2.6.0',
]

setup(name='hypothesis_sqlalchemy',
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
          'Framework :: Hypothesis',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
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
