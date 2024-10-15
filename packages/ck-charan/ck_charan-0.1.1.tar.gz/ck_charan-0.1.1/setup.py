from setuptools import setup, find_packages

setup(
    name='ck-charan',
    version='0.1.1',
    author='Charan Kosari',
    author_email='shivacharankosari099@gmail.com',
    description='A simple ck module with basic functions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    url='https://github.com/charankosari',  # Replace with your GitHub repo URL
)
