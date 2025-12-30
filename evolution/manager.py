import os
import numpy as np

def evolveGeneration(agents, mutationRate=0.05):
    sortedIndices = np.argsort(agents['fitnessScore'])[::-1]
    sortedAgents = agents[sortedIndices]
    
    populationSize = len(agents)
    survivorCount = int(populationSize * 0.1) 
    survivors = sortedAgents[:survivorCount]

    bestScore = survivors[0]['fitnessScore']
    print(f"  -> Best Fitness: {bestScore:.1f} | Worst Survivor: {survivors[-1]['fitnessScore']:.1f}")

    newAgents = np.zeros_like(agents)
    
    
    for i in range(survivorCount):
        newAgents[i] = survivors[i]

        newAgents[i]['fitnessScore'] = 0 
        newAgents[i]['energyLevel'] = 100 
        newAgents[i]['isActive'] = 1.0
    
    for i in range(survivorCount, populationSize):
        parentA = np.random.choice(survivors)
        parentB = np.random.choice(survivors)
        
        childWeights = crossover(parentA['brainWeights'], parentB['brainWeights'])
        childWeights = mutate(childWeights, mutationRate)
        
        newAgents[i]['brainWeights'] = childWeights
        newAgents[i]['isActive'] = 1.0
        newAgents[i]['energyLevel'] = 100
        newAgents[i]['fitnessScore'] = 0
        newAgents[i]['velocity'] = 0 

    return newAgents

def crossover(weightsA, weightsB):
    split = np.random.randint(0, len(weightsA))
    child = np.concatenate((weightsA[:split], weightsB[split:]))

    return child

def mutate(weights, rate):
    mutationMask = np.random.rand(len(weights)) < rate
    noise = np.random.uniform(-1.0, 1.0, size=len(weights))
    weights[mutationMask] += noise[mutationMask]

    return weights

def saveBestBrain(agent, filename="best_brain.npy"):    
    weights = agent['brainWeights']
    np.save(filename, weights)

    print(f"  [Saved] Best brain stored in {filename}")

def loadBestBrain(filename="best_brain.npy"):
    if os.path.exists(filename):
        try:
            weights = np.load(filename)
            print(f"  [Loaded] Brain loaded from {filename}")
            return weights
        except:
            print("  [Error] Could not load brain file.")
            return None
    return None