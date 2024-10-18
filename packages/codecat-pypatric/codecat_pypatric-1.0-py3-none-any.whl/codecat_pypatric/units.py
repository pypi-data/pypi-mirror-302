'''
UNITS.py
========
Created: 30.05.2024

Copyright
Mohammad Yasir
Research Scholar, IIT-D

All rights reserved. No part of this code may be used, modified, shared, or reproduced in any form without express permission of its author.

DESCRIPTION
-----------
Constants and functions that can be used for unit manipulation.
'''

MILLI = 1e-3
MICRO = 1e-6
NANO = 1e-9
ANGSTORM = 1e-10
PICO = 1e-12
FEMTO = 1e-15
FERMI = 1e-15


def jouleToEv(value: float):
    '''
    Converts energy to eV.
    '''
    return value * 1.6021766208e-19


def eVToJoule(value: float):
    '''
    Converts energy to Joule.
    '''
    return value / 1.6021766208e-19


def kelvinToEV(value: float):
    '''
    Converts temperature to eV.
    '''
    return value * 8.6173324e-5


def eVToKelvin(value: float):
    '''
    Converts temperature to Kelvin.
    '''
    return value / 8.6173324e-5