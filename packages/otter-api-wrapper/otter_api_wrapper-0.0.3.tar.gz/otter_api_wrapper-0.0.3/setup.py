from setuptools import setup, find_packages

setup(
    name='otter-api-wrapper',
    version='0.2.0',
    package_dir = {"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        # Add your package dependencies here
        'pandas==2.0.3',
        'requests~=2.27',
        'plotly==5.23.0',
        'kaleido==0.2.1'
    ],
    entry_points={
        'console_scripts': [
            # Add console scripts here
        ],
    },
)
