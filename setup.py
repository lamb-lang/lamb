from setuptools import setup, find_packages

setup(
    name='lamb',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'lamb=lamb.transpiler.cli:main',
        ],
    },
    install_requires=[
        # Any dependencies; for example:
        # 'requests',
    ],
)
