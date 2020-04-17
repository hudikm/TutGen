from setuptools import setup
import pathlib
import glob

data_files = []
directories = glob.glob('templates/')

for directory in directories:
    files = glob.glob(directory+'*')
    data_files.append(('/TutGen/' + directory, files))

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='TutGen',
    url='https://github.com/hudikm/tutgen',
    author='Martin Hudik',
    author_email='martin.hudik@fri.uniza.sk',
    # Needed to actually package something
    packages=['TutGen'],
    # Needed for dependencies
    install_requires=['Jinja2', 'unidiff'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='Generator step by step tutorials from patch file',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
    scripts=['scripts/tutGen.py'],
    # data_files use relative paths(user or system wide):
    # sys.prefix -> /usr/local/
    # sys.USER_DEFINED -> linux  ~/.local/ or win %APPDATA%\Python
    # data_files=[('/TutGen/templates',['templates/files_list.jinja', 'templates/gen_tags.jinja','templates/mkdocs.jinja','templates/mkdocs_obsah.jinja'])],
    data_files=data_files
)
