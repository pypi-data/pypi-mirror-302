from setuptools import setup, find_packages

setup(
    name='frequency_encoder',
    version='0.1.0',
    description='A frequency encoder for pandas DataFrames compatible with scikit-learn pipelines.',
    author='Cristopher Lincoleo Oyarce',
    author_email='cris.lincoleo@gmail.com',
    url='https://github.com/crisbebop/frequency_encoder',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'scikit-learn',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
)
