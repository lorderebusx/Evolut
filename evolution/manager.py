import os
import numpy as np

def evolveGeneration(agents, mutationRate=0.05):
    """
    Sorts agents by fitness, clones the best, and mutates the rest.
    """
    # 1. Sort descending by fitnessScore
    # We use a structured array, so we sort by the field name
    sortedIndices = np.argsort(agents['fitnessScore'])[::-1]
    sortedAgents = agents[sortedIndices]
    
    populationSize = len(agents)
    survivorCount = int(populationSize * 0.1) # Top 10% survive
    survivors = sortedAgents[:survivorCount]
    
    # Print stats to console so we can track progress
    bestScore = survivors[0]['fitnessScore']
    print(f"  -> Best Fitness: {bestScore:.1f} | Worst Survivor: {survivors[-1]['fitnessScore']:.1f}")

    # 2. Create the next generation buffer
    newAgents = np.zeros_like(agents)
    
    # --- ELITISM: Keep the winners ---
    for i in range(survivorCount):
        newAgents[i] = survivors[i]
        # Reset stats for the new round, but KEEP the 'brainWeights'
        newAgents[i]['fitnessScore'] = 0 
        newAgents[i]['energyLevel'] = 100 
        newAgents[i]['isActive'] = 1.0

    # --- BREEDING: Fill the rest ---
    for i in range(survivorCount, populationSize):
        # Pick two random parents from the elite list
        parentA = np.random.choice(survivors)
        parentB = np.random.choice(survivors)
        
        # Crossover: Mix their brains
        childWeights = crossover(parentA['brainWeights'], parentB['brainWeights'])
        
        # Mutation: Add random changes
        childWeights = mutate(childWeights, mutationRate)
        
        # Assign to new agent
        newAgents[i]['brainWeights'] = childWeights
        newAgents[i]['isActive'] = 1.0
        newAgents[i]['energyLevel'] = 100
        newAgents[i]['fitnessScore'] = 0
        newAgents[i]['velocity'] = 0 # Reset speed

    return newAgents

def crossover(weightsA, weightsB):
    # Split the DNA at a random point
    split = np.random.randint(0, len(weightsA))
    child = np.concatenate((weightsA[:split], weightsB[split:]))
    return child

def mutate(weights, rate):
    # Create a mask (True/False) for which genes to mutate
    mutationMask = np.random.rand(len(weights)) < rate
    
    # Add random noise (-0.5 to 0.5) to those genes
    noise = np.random.uniform(-1.0, 1.0, size=len(weights))
    
    weights[mutationMask] += noise[mutationMask]
    return weights

def saveBestBrain(agent, filename="best_brain.npy"):
    """
    Saves the weights of a single agent to a binary file.
    """
    # specific Agent -> .brainWeights -> numpy array
    weights = agent['brainWeights']
    np.save(filename, weights)
    print(f"  [Saved] Best brain stored in {filename}")

def loadBestBrain(filename="best_brain.npy"):
    """
    Tries to load brain weights from a file.
    Returns the weights if found, otherwise returns None.
    """
    if os.path.exists(filename):
        try:
            weights = np.load(filename)
            print(f"  [Loaded] Brain loaded from {filename}")
            return weights
        except:
            print("  [Error] Could not load brain file.")
            return None
    return None