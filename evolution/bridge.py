import ctypes
import numpy as np
import os

BRAIN_SIZE = 66

class AgentStruct(ctypes.Structure):
    _fields_ = [
        ("isActive", ctypes.c_float),
        ("energyLevel", ctypes.c_float),
        ("fitnessScore", ctypes.c_float),
        ("posX", ctypes.c_float),
        ("posY", ctypes.c_float),
        ("rotationAngle", ctypes.c_float),
        ("velocity", ctypes.c_float),
        ("brainWeights", ctypes.c_float * BRAIN_SIZE)
    ]

class FoodStruct(ctypes.Structure):
    _fields_ = [
        ("posX", ctypes.c_float),
        ("posY", ctypes.c_float),
        ("isEaten", ctypes.c_float)
    ]

# Load the library
libPath = os.path.abspath("build/simulation.so")
simulationLib = ctypes.CDLL(libPath)

# Tell ctypes the argument types for our C function
simulationLib.updateSimulation.argtypes = [
    ctypes.POINTER(AgentStruct), 
    ctypes.c_int, 
    ctypes.POINTER(FoodStruct), 
    ctypes.c_int, 
    ctypes.c_float
]