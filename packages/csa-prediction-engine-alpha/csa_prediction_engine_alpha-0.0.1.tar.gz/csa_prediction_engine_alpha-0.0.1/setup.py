from setuptools import setup, find_packages


setup(
    name='csa_prediction_engine_alpha',
    version="0.0.1",
    packages=find_packages(include=['csa_prediction_engine', 'csa_prediction_engine.*']),
    install_requires=[
        'numpy>=2.1',
        'requests',
        'csa_common_lib_alpha'
    ]
)

# setup(
#     name='csa_common_lib_alpha',
#     version="0.0.1",
#     packages=find_packages(include=['csa_common_lib', 'csa_common_lib.*']),
#     install_requires=[
#         'boto3==1.35.20',
#         'numpy==2.1.1',
#         'openpyxl==3.1.5',
#         'pandas==2.2.2',
#         'plotnine==0.13.6',
#         'Requests==2.32.3',
#     ]
# )