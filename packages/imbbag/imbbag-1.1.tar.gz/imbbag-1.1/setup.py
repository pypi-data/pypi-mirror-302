from setuptools import setup, find_packages

setup(
    name='imbbag',
    version='1.1',
    author='Yousef Abdi',
    author_email='yousef.abdi@gmail.com',
    description='Package contains a collection of bagging ensemble algorithms for imbalanced data',
    packages = find_packages(),
    package_data={
        'imbbag': ['config/rules.yml'],
    },
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yousefabdi/imbbag',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        'scikit-learn',
        'imblearn',
        'numpy',
        'scipy',
        'PyGAD',
        'mlxtend',
        'scikit-learn-intelex',
        'ARFS'
    ],
)