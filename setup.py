from setuptools import setup, find_packages

# TODO create config folder

if __name__ == '__main__':
    setup(
        name='ifttt',
        version="0.1",
        description="ifttt: home made email notification system for RSS feeds",
        author="Ce Gao",
        install_requires=[
            'yagmail >= 0.5.140',
            'feedparser >= 5.2.1',
            'jinja2 >= 2.8'
        ],
        packages=find_packages(exclude="tests"),
        package_data={'ifttt': ['templates/*']},
        entry_points={
            'console_scripts': ['ifttt=ifttt:main']
        }
    )
