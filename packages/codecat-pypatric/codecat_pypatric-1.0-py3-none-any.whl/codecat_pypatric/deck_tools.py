'''
DECK TOOLS.py
=============
Created: 03.07.2024

Copyright
Mohammad Yasir
Research Scholar, IIT-D

All rights reserved. No part of this code may be used, modified, shared, or reproduced in any form without express permission of its author.

DESCRIPTION
-----------
Tools to help write the deck
'''


from inspect import signature
from typing import Callable, Tuple

from codecat_pypatric.electric import *
from codecat_pypatric.magnetic import *
from codecat_pypatric.classes import *
from codecat_pypatric.keys import *


Control = {}
Particle = {}
Fields = {}
Output = {}


def __showError(errorMessage: str, errorCode: int):
    print(f'\nERROR {errorCode} ENCOUNTERED WHILE PARSING INPUT SCRIPT:\n{errorMessage}\n')
    exit(errorCode)


def createControl(
        timeStep: float, numiterations: int,
        integrator: int, readoutFreq: int):
    '''
    Create the control dict.
    Parameters:
        timeStep : float The time step dt.
        numiterations : int The number of iterations to run the program for.
        integrator : int The numerical integration method to use. Must be one of BORIS, VAY, or HIGUERA_CARY.
        readoutFreq : int The frequency at which to show a small output message. Zero or negative to turn off.
    '''

    # Validate inputs.
    if timeStep <= 0:
        __showError('Time step must be a positive float', 101)
    if numiterations <= 0:
        __showError('Number of iterations must be a positive integer', 101)
    if integrator not in [BORIS, VAY, HIGUERA_CARY]:
        __showError('Invalid integrator. Must be one of BORIS, VAY, or HIGUERA_CARY.', 101)

    global Control
    Control[TIME_STEP] = timeStep
    Control[NUM_ITERS] = numiterations
    Control[INTEGRATOR] = integrator
    Control[READOUT_FREQ] = readoutFreq



def createParticles(
        mass: float, charge: float, particleCount: int,
        initialPosition: Tuple,
        initialVelocity: Tuple):
    '''
    Create the particle dict.
    Parameters:
        mass : float The mass of the particle in multiple of electronic mass.
        charge : float The charge of the particle in multiples of fundamental charge.
        initialPosition : Tuple The initial position(s) of the particle(s)
        initialVelocity : Tuple The initial velocity(s) of the particle(s)
    '''

    # Validate inputs.
    if mass <= 0:
        __showError('Mass must be a positive float', 102)
    if particleCount <= 0:
        __showError('Particle count must be a positive integer', 102)
    if len(initialPosition) < 1:
        __showError('Initial position must be a tuple with at least one element', 102)
    if len(initialVelocity) < 1:
        __showError('Initial velocity must be a tuple with at least one element', 102)
    
    # Ensure that the initial positions provided are in correct format
    for r in initialPosition:
        if type(r) not in (Static, Uniform, Random):
            __showError('Initial positions must be Static, Uniform, or Random objects.', 102)
    
    for v in initialVelocity:
        if type(v) not in (Static, Uniform, Maxwellian):
            __showError('Initial velocities must be Static, Uniform, or Maxwellian objects.', 102)
        

    global Particle
    Particle[MASS] = mass
    Particle[CHARGE] = charge
    Particle[PARTICLE_COUNT] = particleCount
    Particle[INITIAL_POSITION] = initialPosition
    Particle[INITIAL_VELOCITY] = initialVelocity


def createFields(
        electricFields: Tuple | Callable,
        magneticFields: Tuple | Callable):
    '''
    Create the fields dict. 
    Parameters:
        electricFields : Tuple | callable The electric field(s). The total field 
        magneticFields : Tuple | callable The magnetic field(s)
    '''

    supportedEleFields = (Static, SinField, GaussField, PointCharge, ElectricDipole)
    supportedMagFields = (Static, SinField, GaussField, Coil)

    # Validate inputs.
    if electricFields is None:
        electricFields = tuple([])

    elif isinstance(electricFields, Tuple):
        for e in electricFields:
            if type(e) not in supportedEleFields:
                __showError(f'Electric field must be one of {supportedEleFields} or be a callable function.', 103)
    else:
        if len(signature(electricFields).parameters) != 4:
            __showError('Electric field as a function must take four parameters: x, y, z, and t.', 103)

    if magneticFields is None:
        magneticFields = tuple([])

    elif isinstance(magneticFields, Tuple):
        for b in magneticFields:
            if type(b) not in supportedMagFields:
                __showError(f'Magnetic field must be one of {supportedMagFields} or be a callable function.', 103)

    else:
        if len(signature(magneticFields).parameters) != 4:
            __showError('Magnetic field as a function must take four parameters: x, y, z, and t.', 103)

        
    global Fields
    Fields[E_FIELD] = electricFields
    Fields[B_FIELD] = magneticFields


def createOutput(
        fileName: str, filePath: str,
        fileHeaders: Tuple[str, ...], dumpInfoFile: bool, dumpVariables: Tuple[str, ...]):
    '''
    Create the output dict.
    Parameters:
        fileName : str The name of the output file.
        filePath : str The path to the output file.
        fileHeaders : Tuple[str,...] The headers to include in the info file.
        dumpInfoFile : bool Whether to dump info file.
        dumpVariables : Tuple[str,...] The variables to dump in the output file.
    '''

    # Validate inputs.
    supportedDumpVariables = (
        POS_X, POS_Y, POS_Z, 
        VEL_X, VEL_Y, VEL_Z, 
        E_FIELD_X, E_FIELD_Y, E_FIELD_Z,
        B_FIELD_X, B_FIELD_Y, B_FIELD_Z,
        GAMMA)

    if not fileName:
        __showError('Output file name cannot be empty.', 104)
        exit(104)
    for v in dumpVariables:
        if v not in supportedDumpVariables:
            __showError('Invalid dump variable. Must be one of {supportedDumpVariables}.', 104)

    global Output
    Output[FILENAME] = fileName
    Output[FILEPATH] = filePath
    Output[FILE_HEADER] = fileHeaders
    Output[DUMP_INFO_FILE] = dumpInfoFile
    Output[DUMP_VARIABLES] = dumpVariables