from setuptools import setup, find_packages
import os

dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(dir, 'ioiocore', 'requirements.txt'), 'r') as f:
    requirements = f.read().splitlines()

with open(os.path.join(dir, 'README.md'), encoding='utf-8') as rm:
    description = rm.read()

ver = {}
with open(os.path.join(dir, 'ioiocore', '__version__.py')) as v:
    exec(v.read(), ver)

pkg = find_packages()

setup(
    name='ioiocore',
    version=ver['__version__'],
    packages=pkg,
    long_description=description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    classifiers=[
        #'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        #'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',

        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',

        "Programming Language :: Python :: 3",
    ],
    author='g.tec medical engineering GmbH',
    author_email='support@gtec.at',
    description='A realtime processing framework for python',
    license='MIT',
    url='https://www.gtec.at',
)