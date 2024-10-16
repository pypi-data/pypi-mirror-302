from setuptools import setup, find_packages

setup(
    name='subweb',
    version='2.0.0',
    description='A package for scanning subdomains and collecting website information.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='MrFidal',
    author_email='mrfidal@proton.me',
    url='https://github.com/ByteBreach/subweb',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    keywords='subdomain scanning web scraping information',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
    ],
)
