from setuptools import setup, find_packages

setup(
    name='roborregos-metrics-server',
    version='0.0.3',
    packages=find_packages(),
    install_requires=[
        'requests',
        'fastapi',
        'pydantic',
        'uvicorn',
        'pymongo',
        'psutil'
    ],
    entry_points={
        'console_scripts': [
            'robometrics-server = robometrics.server.IntakeAndServe:main'
        ]
    }
)
