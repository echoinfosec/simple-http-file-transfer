from setuptools import setup

setup(
    name='httpserver',
    version='1.0.0',
    description='A simple HTTP server made to transfer files',
    author='echo',
    url='https://github.com/echoinfosec/simple-http-server',
    install_requires=[
        'Flask==3.0.1'
    ],
    entry_points= {
        'console_scripts': ['httpserver=server.server:main']
    }
)
