from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='thecalcLIB',
    version='0.0.1',
    description='This is a calculator package',
    Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Freddy Frolov',
    author_email='freddyfrolov383@gmail.com',
    License='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requiers=['']
)