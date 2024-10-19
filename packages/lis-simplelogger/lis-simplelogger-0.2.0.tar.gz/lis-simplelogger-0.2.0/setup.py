from setuptools import setup, find_packages

setup(
    name='lis-simplelogger',        
    version='0.2.0',                   
    packages=find_packages(),
    description='Simple Logger for LIS.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/timothyjchun/lis-simplelogger',
    author='Timothy Chun',
    author_email='timchun0212@gmail.com',
    license='MIT',                   # License for your package
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',         # Python version requirement
    install_requires=[],             # Dependencies (if any)
)
