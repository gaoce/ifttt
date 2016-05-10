from setuptools import setup, find_packages
import os

# Create config folder
home_dir = os.path.join(os.path.expanduser('~'), '.ifttt')
if not os.path.exists(home_dir):
    os.mkdir(home_dir)

if __name__ == '__main__':
    setup(
        name='ifttt',
        version="0.1",
        description="ifttt: home made email notification system for RSS feeds",
        author="Ce Gao",
        install_requires=[
            'yagmail >= 0.5.140',
            'feedparser >= 5.2.1',
            'jinja2 >= 2.8',
            'six >= 1.10.0'
        ],
        packages=find_packages(exclude=("tests",)),
        package_data={'ifttt': ['templates/*']},
        entry_points={
            'console_scripts': ['ifttt=ifttt:main']
        }
    )
