from setuptools import setup, find_packages

setup(
    name='demox2004',  # The name of your package
    version='0.1',
    packages=find_packages(),
    description='A package that contains DFS, BFS, and other example programs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
