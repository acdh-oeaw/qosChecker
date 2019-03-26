from setuptools import setup, find_packages


setup(
    name="qosChecker",
    version="0.1.0",
    packages=find_packages(),
    scripts=['scripts/qos-check'],
    install_requires=['paramiko'],

    author="Mateusz Zoltak",
    author_email="mzoltak@oeaw.ac.at",
    description="Package checking ACDH servise QoS",
    license="MIT",
    project_urls={
        "Bug Tracker": "https://github.com/acdh-oeaw/qosChecker/issues",
        "Documentation": "https://github.com/acdh-oeaw/qosChecker",
        "Source Code": "https://github.com/acdh-oeaw/qosChecker",
    }
)
