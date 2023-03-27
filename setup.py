from setuptools import setup, find_packages

setup(
    name='finx',
    version='0.0.1',
    author='Your Name',
    author_email='your@email.com',
    description='A private Python package for financial calculations',
    packages=find_packages(),
    install_requires=[
        'python-dateutil',
        'nelson-siegel-svensson'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
