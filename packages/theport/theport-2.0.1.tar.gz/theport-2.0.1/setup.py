from setuptools import setup, find_packages

setup(
    name='theport',
    version='2.0.1',
    author='MrFidal',
    author_email='mrfidal@proton.me',
    description='A library for scanning ports and identifying services',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ByteBreach/theport',  
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests', 
    ],
)
