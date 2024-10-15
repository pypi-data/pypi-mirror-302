from setuptools import setup, find_packages

setup(
    name='roborregos-metrics-server',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'fastapi',
        'pydantic',
        'uvicorn'
    ],
    entry_points={
        'console_scripts': [
            'robometrics-server = robometrics.server.IntakeAndServe:main'
        ]
    }
)
