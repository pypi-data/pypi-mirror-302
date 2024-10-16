from setuptools import setup, find_packages

setup(
    name='Tokenize2',
    version='2.0.3',
    description='A byte-level BPE tokenizer for efficient text processing',
    author='TNSA AI',
    author_email='thishyakethabimalla@gmail.com',
    packages=find_packages(),
    install_requires=[],
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/TnsaAi/Tokenize2',  # Replace with your GitHub repo
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
