'''
ELECTRIC.py
===========
Created: 18.06.2024

Copyright
Mohammad Yasir
Research Scholar, IIT-D

All rights reserved. No part of this code may be used, modified, shared, or reproduced in any form without express permission of its author.

DESCRIPTION
-----------
Contains classes that describe electric field geometries
'''


# The static class is already defined for positions and velocities. 
# We just need it here to make the file complete.
from codecat_pypatric.classes import Static, SinField, GaussField


class PointCharge:
    '''
    Represents a point charge field.
    '''
    def __init__(self, x: float, y: float , z: float, q: float):
        '''
        Parameters
        ----------
        x: The x coordinate of the point charge's location.
        y: The y coordinate of the point charge's location.
        z: The z coordinate of the point charge's location.
        q: The charge of the point charge.
        '''
        self.x = x
        self.y = y
        self.z = z
        self.q = q

    def __str__(self) -> str:
        return f'PointCharge({self.x, self.y, self.z, self.q})'
    
    def __repr__(self) -> str:
        return self.__str__()
    


class ElectricDipole:
    '''Represents an electric dipole placed at a certain location.'''
    def __init__(self, p: tuple[float, float, float], r: tuple[float, float, float]):
        '''
        Parameters
        ----------
        p: The electric dipole moment in vector form.
        r: The location of the midpoint of the electric dipole.
        '''
        self.p = p
        self.r = r
    
    def __str__(self) -> str:
        return f'ElectricDipole{*self.p, *self.r}'
    
    def __repr__(self) -> str:
        return self.__str__()
