from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def readme():
    with open('README.md') as readme_file:
        return readme_file.read()


setup(
    name='easyrpc',
    version='0.0.0',
    description='Common Thrift RPC client and proper handling for it',
    long_description=readme(),
    keywords='thrift rpc client',
    url='http://github.com/silver-saas/silver',
    author='Horia Coman',
    author_email='horia141@gmail.com',
    license='All right reserved',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    install_requires=[
        'thrift==0.9.3',
        'thriftplus==0.0.2',
        ],
    test_suite='tests',
    tests_require=[
        'coverage==4.1b1',
        'portpicker==1.1.0',
        'thriftgen_easyrpc_tests_adder==0.0.0',
    ],
    include_package_data=True,
    zip_safe=False
)
