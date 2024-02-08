
from setuptools import setup, find_packages
from jhta.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='jhta',
    version=VERSION,
    description='Assists in commont tasks while teaching a class using JupyterHub',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Gleb Dovzhenko',
    author_email='dovjenko.g@gmail.com',
    url='https://github.com/glebdovzhenko/JHubTA',
    license='GNU GPLv3',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'jhta': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        jhta = jhta.main:main
    """,
)
