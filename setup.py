from distutils.core import setup
# TEST Package
# setup(
#     name='leccap-test',
#     packages=['leccap'],
#     version='0.0.5',
#     description='Umich lecture downloader',
#     author='Jackie Zhang',
#     author_email='jackierw@umich.edu',
#     url='https://github.com/ReactiveXYZ-Dev/dleccap',
#     keywords=['leccap', 'downloader', 'lecture', 'umich'],
#     license="CC0",
#     classifiers=["Programming Language :: Python :: 2"],
#     scripts=['bin/leccap'],
#     package_data={
#         'leccap': ['*.json'],
#     },
#     install_requires=['requests', 'wget', 'colorama', 'future']
# )

setup(
    name='leccap',
    packages=['leccap'],
    version='0.0.5',
    description='Umich lecture downloader',
    author='Jackie Zhang',
    author_email='jackierw@umich.edu',
    url='https://github.com/ReactiveXYZ-Dev/dleccap',
    keywords=['leccap', 'downloader', 'lecture', 'umich'],
    license="CC0",
    scripts=['bin/leccap'],
    package_data={
        'leccap': ['*.json'],
    },
    install_requires=['requests', 'wget', 'colorama', 'future']
)
