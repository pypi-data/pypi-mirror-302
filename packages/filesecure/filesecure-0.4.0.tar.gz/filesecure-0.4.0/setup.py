from setuptools import setup, find_packages

setup(
    name='filesecure',
    version='0.4.0',
    description='A file encryption and decryption tool',
    author='Tahar BOUNSIAR',
    author_email='tbounsiar@gmail.com',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tbounsiar/filecrypt',
    install_requires=[
        'cryptography',
    ],
    entry_points={
        'console_scripts': [
            'filesecure = filesecure:filesecure',
        ],
    },
)
