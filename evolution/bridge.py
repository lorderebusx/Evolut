import ctypes
import os

class AgentStruct(ctypes.Structure):
    _fields_ = [
        ("isActive", ctypes.c_float),
        ("posX", ctypes.c_float),
        ("posY", ctypes.c_float),
        ("rotationAngle", ctypes.c_float),
        ("energyLevel", ctypes.c_float),
        ("velocity", ctypes.c_float),
        ("brainWeights", ctypes.c_float * 56),
        ("fitnessScore", ctypes.c_float)
    ]

class FoodStruct(ctypes.Structure):
    _fields_ = [
        ("posX", ctypes.c_float),
        ("posY", ctypes.c_float),
        ("isEaten", ctypes.c_float)
    ]

class PredatorStruct(ctypes.Structure):
    _fields_ = [
        ("posX", ctypes.c_float),
        ("posY", ctypes.c_float),
        ("velocity", ctypes.c_float)
    ]

BRAIN_SIZE = 56 

so_path = os.path.abspath("evolution/build/simulation.so") 
if not os.path.exists(so_path):
    so_path = os.path.abspath("build/simulation.so")

simulationLib = ctypes.CDLL(so_path)

simulationLib.updateSimulation.argtypes = [
    ctypes.POINTER(AgentStruct),
    ctypes.c_int,
    ctypes.POINTER(FoodStruct),
    ctypes.c_int,
    ctypes.POINTER(PredatorStruct),
    ctypes.c_int,
    ctypes.c_float
]