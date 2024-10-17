# setup.py
from setuptools import setup, find_packages

setup(
    name='extractimail',
    version='1.0.0',
    author='Federico Toscano',
    author_email='federico.toscano@axpo.com',
    description='A tool to automatically recollect emails and save attachments.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'pywin32',
        'PyPDF2',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'extractimail=extractimail.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.6',
)
