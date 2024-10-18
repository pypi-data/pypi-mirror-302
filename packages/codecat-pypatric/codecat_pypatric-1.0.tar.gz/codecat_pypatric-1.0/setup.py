'''
SETUP.py
========
Created: 18.06.2024

Copyright
Mohammad Yasir
Research Scholar, IIT-D

All rights reserved. No part of this code may be used, modified, shared, or reproduced in any form without express permission of its author.

DESCRIPTION
-----------
Setup file
'''

from setuptools import setup


setup(
    name='codecat_pypatric',
    version='1.0',
    packages=['codecat_pypatric'],

    author='Mohammad Yasir',
    author_email='yasir.iitd@outlook.com',
    
    license='GNU GPL Version 3',
    url='https://github.com/hafizmdyasir/codecat_pypatric',
    description='Helper package for the PaTriC particle tracking code.',
    
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)