from setuptools import setup, find_packages


setup(
    name='csa_prediction_engine_alpha',
    version="0.1",
    packages=find_packages(include=['csa_prediction_engine', 'csa_prediction_engine.*']),
    install_requires=[
        'numpy>=2.1',
        'requests',
        'csa_common_lib_alpha'
    ]
)