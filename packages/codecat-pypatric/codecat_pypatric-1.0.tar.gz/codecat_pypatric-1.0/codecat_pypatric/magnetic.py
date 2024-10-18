'''
MAGNETIC.py
===========
Created: 18.06.2024

Copyright
Mohammad Yasir
Research Scholar, IIT-D

All rights reserved. No part of this code may be used, modified, shared, or reproduced in any form without express permission of its author.

DESCRIPTION
-----------
Contains classes that describe magnetic field geometries
'''


# The static class is already defined for positions and velocities. 
# We just need it here to make the file complete.
from codecat_pypatric.classes import Static, SinField, GaussField


class Coil:
    '''
    Represents a coil of given radius, carrying a certain current, placed at a point along the z-axis. No other axis is supported at the moment.
    '''
    def __init__(self, radius: float, current: float, zPosition: float = 0):
        '''
        Parameters
        ----------
        radius : float Radius of the coil.
        current : float Current flowing through the coil. It is redundant to include number of turns since that can easily be incorporated by multiplying the current with the number of turns.
        zPosition : float Position of the coil along the z-axis.
        '''
        self.radius = radius
        self.current = current
        self.zPosition = zPosition

    def __str__(self) -> str:
        return f"Coil({self.radius}, {self.current}, {self.zPosition})"
    
    def __repr__(self) -> str:
        return self.__str__()