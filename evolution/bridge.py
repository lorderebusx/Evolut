import ctypes
import os

# 1. Define C Structures (MUST MATCH simulation.h EXACTLY)
class AgentStruct(ctypes.Structure):
    _fields_ = [
        ("isActive", ctypes.c_float),
        ("posX", ctypes.c_float),
        ("posY", ctypes.c_float),
        ("rotationAngle", ctypes.c_float),
        ("energyLevel", ctypes.c_float),
        ("velocity", ctypes.c_float),
        ("brainWeights", ctypes.c_float * 56), # Size 56
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

# 2. Load the DLL
BRAIN_SIZE = 56 
# Use .so because that is what your build produces
so_path = os.path.abspath("evolution/build/simulation.so") 
if not os.path.exists(so_path):
    # Fallback to just build/simulation.so if the path is relative
    so_path = os.path.abspath("build/simulation.so")

simulationLib = ctypes.CDLL(so_path)

# 3. Define Argument Types
simulationLib.updateSimulation.argtypes = [
    ctypes.POINTER(AgentStruct),
    ctypes.c_int,
    ctypes.POINTER(FoodStruct),
    ctypes.c_int,
    ctypes.POINTER(PredatorStruct),
    ctypes.c_int,
    ctypes.c_float
]