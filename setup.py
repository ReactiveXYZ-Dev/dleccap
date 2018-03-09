from distutils.core import setup
setup(
    name='leccap',
    packages=['leccap'],
    version='2.0.0',
    description='Umich lecture downloader',
    author='Jackie Zhang',
    author_email='jackierw@umich.edu',
    url='https://github.com/ReactiveXYZ-Dev/dleccap',
    keywords=['leccap', 'downloader', 'lecture', 'umich'],
    license="CC0",
    classifiers=["Programming Language :: Python :: 2"],
    scripts=['bin/leccap'],
    include_package_data=True
)
