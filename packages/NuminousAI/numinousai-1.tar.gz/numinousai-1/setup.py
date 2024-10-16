from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='NuminousAI',
    version='1',
    description='This Python package designed to provide a comprehensive interface for interacting with various AI models and performing a range of functionalities such as URL interaction, system command execution, and more.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sujal Rajpoot',
    author_email='sujalrajpoot70@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests>=2.0.0', 'click>=8.1.7', 'appdirs>=1.4.4', 'tqdm>=4.66.4', 'selenium>=4.20.0', 'cerebras_cloud_sdk>=1.5.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
