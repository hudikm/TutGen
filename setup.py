from setuptools import setup
import pathlib

# datadir = os.path.join('templates')
# datafiles = [(d, [os.path.join(d,f) for f in files])
#     for d, folders, files in os.walk(datadir)]

data_files__=[(str(pathlib.Path.home().joinpath('.local/TutGen/templates')),['templates/files_list.jinja', 'templates/gen_tags.jinja','templates/mkdocs.jinja','templates/mkdocs_obsah.jinja'])]
print(data_files__)

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
    data_files=data_files__,
)
