from setuptools import setup, find_packages

setup(
    name='edalib',
    version='0.1',
    packages=find_packages(),
    description='This is just my library for exploratory data analysis. Nothing fancy.',
    long_description="This is just my library for exploratory data analysis. Nothing fancy.",  # Just a short description
    long_description_content_type='text/plain',  # Use 'text/plain' since it’s a simple string
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/edalib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
