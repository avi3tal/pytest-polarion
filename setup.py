from setuptools import setup

setup(
    name="pytest_polarion",
    use_scm_version={'write_to': 'pytest_polarion/_version.py'},
    packages=['pytest_polarion'],
    long_description=open('README.rst').read(),
    author='Avi Tal',
    author_email='atal@redhat.com',
    entry_points={
        'pytest11': [
            'pytest_polarion = pytest_polarion.plugin',
        ]
                   },
    install_requires=['pytest>=2.4.2'],
    classifiers=['Private :: Do Not Upload'],  # hack to avoid uploading to pypi
    setup_requires=['setuptools_scm'],
)