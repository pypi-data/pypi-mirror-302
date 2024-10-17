# setup.py

from setuptools import setup, find_packages

setup(
    name="inference_worker",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "click",
        "pika",
        "requests",
    ],
    package_data={
        'inference_worker': ['boilerplate/**/*']
    },
    entry_points={
        "console_scripts": [
            "inference=inference_worker.cli:main",
        ],
    },
)
