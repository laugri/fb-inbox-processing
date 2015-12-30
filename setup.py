from setuptools import setup

setup(
    name='fb-inbox-processing',
    version='0.1',
    description='Pulls insights from Facebook inbox data.',
    url='https://github.com/laugri/fb-inbox-processing',
    author='Laurent Grima',
    author_email='grima.laurent@gmail.com',
    license='MIT',
    packages=['fbinboxprocessing'],
    install_requires=['nltk', 'beautifulsoup4'],
    test_suite='nose.collector',
    tests_require=['nose'],
)