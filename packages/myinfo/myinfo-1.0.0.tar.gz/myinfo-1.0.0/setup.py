from setuptools import setup, find_packages

setup(
    name='myinfo',
    version='1.0.0',
    description='A package to retrieve WHOIS and IP information',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='MrFidal',
    author_email='mrfidal@proton.me',
    packages=find_packages(),
    install_requires=[
        'whois',
        'ipwhois',
        'dnspython',
    ],
    python_requires='>=3.6',
)
