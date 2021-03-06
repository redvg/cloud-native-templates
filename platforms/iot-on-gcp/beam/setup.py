import setuptools

packages = [
        "simplejson==3.16.0",
        "strict-rfc3339==0.7"
        ]

setuptools.setup(
    name='telemetry_etl',
    version='0.1',
    install_requires=packages,
    packages=setuptools.find_packages(),
)