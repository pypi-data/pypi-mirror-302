from setuptools import setup

setup(
    name='rsstools',
    version='0.2.0',
    description='A simple CLI tool for creating and managing RSS feeds',
    author='sctech-tr',
    author_email='gamerselimiko@gmail.com',
    packages=['rsstools'],
    entry_points={
        'console_scripts': [
            'rsstools=rsstools.__main__:main',
        ],
    },
    install_requires=[
        'feedgen',
    ],
)
