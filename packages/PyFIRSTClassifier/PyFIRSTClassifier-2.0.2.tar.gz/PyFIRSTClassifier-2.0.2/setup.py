from setuptools import setup, find_packages

setup(
    name='PyFIRSTClassifier',
    version='2.0.2',
    description='Automated morphological classification of Compact and Extended radio sources using Deep Convolutional Neural Networks',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Wathela Alhassan',
    author_email='wathelahamed@gmail.com',
    url='https://github.com/wathela/FIRSTClassifier', 
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'pandas==2.0.3',
        'numpy==1.24.3',
        'matplotlib==3.7.5',
        'scipy==1.10.1',
        'astropy==5.2.2',
        'pyvo==1.5.2',
        'scikit-image==0.21.0',
        'keras==2.13.1',
        'tensorflow==2.13.1'
    ],
    entry_points={
        'console_scripts': [
            'first_classifier=PyFIRSTClassifier.FIRSTClassifier:main',
        ],
    },
)

