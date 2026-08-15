from setuptools import find_packages, setup

project_base_url = 'https://github.com/lycantropos/hypothesis_sqlalchemy/'


setup(
    packages=find_packages(exclude=('tests', 'tests.*')),
    url=project_base_url,
    download_url=project_base_url + 'archive/master.zip',
)
