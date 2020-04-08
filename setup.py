from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='PatchCreator',
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
    scripts=['scripts/tutGen.py']
)
