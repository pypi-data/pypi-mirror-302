from setuptools import setup, find_packages

setup(
    name='eplremade',
    version='1.0.0',
    author='Silicon Yang',
    author_email='yangsilicon@gmail.com',
    description='Every Python Library Remade, a project to improve base Python modules and libraries.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Silicon27/EPLRemade',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)