import pygame
import numpy as np
import ctypes
from evolution.bridge import AgentStruct, FoodStruct, PredatorStruct, simulationLib, BRAIN_SIZE
from evolution.manager import evolveGeneration, saveBestBrain, loadBestBrain, mutate

def runSimulation():

    with open("simulation_log.txt", "w") as f:
        f.write("Generation:     | Reason:              | Best Fitness Score:      | Worst Survivor Score:     \n")
        f.write("-" * 93 + "\n")

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    numAgents = 50
    numFood = 120
    
    agents = np.zeros(numAgents, dtype=AgentStruct)
    food = np.zeros(numFood, dtype=FoodStruct)
    
    savedBrain = loadBestBrain("best_brain.npy")

    for a in agents:
        a['isActive'] = 1.0
        a['energyLevel'] = 100.0
        a['posX'] = np.random.uniform(100, 700)
        a['posY'] = np.random.uniform(100, 500)
        a['rotationAngle'] = np.random.uniform(0, 2 * np.pi)
        
        if savedBrain is not None and savedBrain.shape[0] == BRAIN_SIZE:
            a['brainWeights'] = savedBrain.copy()            
            if a is not agents[0]: 
                 noise = np.random.uniform(-0.1, 0.1, size=BRAIN_SIZE)
                 a['brainWeights'] += noise
        else:         
            randomWeights = np.random.uniform(-1.0, 1.0, size=BRAIN_SIZE)
            for i in range(BRAIN_SIZE):
                a['brainWeights'][i] = randomWeights[i]

    
    for f in food:
        f['posX'] = np.random.uniform(50, 750)
        f['posY'] = np.random.uniform(50, 550)
        f['isEaten'] = 0.0
    
    numPredators = 3 
    predators = np.zeros(numPredators, dtype=PredatorStruct)
    
    for p in predators:
        p['posX'] = np.random.uniform(0, 800)
        p['posY'] = np.random.uniform(0, 600)
        p['velocity'] = 2.0

    generation = 1
    frameCount = 0
    GEN_DURATION = 60 * 15 
    
    print(f"--- G E N E R A T I O N     {generation} ---")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        simulationLib.updateSimulation(
            agents.ctypes.data_as(ctypes.POINTER(AgentStruct)),
            numAgents,
            food.ctypes.data_as(ctypes.POINTER(FoodStruct)),
            numFood,
            predators.ctypes.data_as(ctypes.POINTER(PredatorStruct)), 
            numPredators, 
            0.5 
        )
        
        screen.fill((20, 20, 20))
        
        kingIndex = -1
        highestScore = -1.0
        
        for i in range(numAgents):
            if agents[i]['isActive'] > 0.5:
                if agents[i]['fitnessScore'] > highestScore:
                    highestScore = agents[i]['fitnessScore']
                    kingIndex = i
        
        for i in range(numAgents):
            a = agents[i]
            if a['isActive'] > 0.5:
                color = (200, 200, 200) 
                radius = 4
                thickness = 1    
                
                if i == kingIndex:
                    color = (255, 215, 0) 
                    radius = 6            
                    thickness = 0
                    
                    pygame.draw.circle(screen, (255, 255, 0), (int(a['posX']), int(a['posY'])), 10, 1)
                
                noseX = a['posX'] + np.cos(a['rotationAngle']) * 10
                noseY = a['posY'] + np.sin(a['rotationAngle']) * 10
                
                startPos = (int(a['posX']), int(a['posY']))
                endPos = (int(noseX), int(noseY))
                
                pygame.draw.line(screen, color, startPos, endPos, 2)
                pygame.draw.circle(screen, color, startPos, radius, thickness)

        for f in food:
            if f['isEaten'] < 0.5:
                pygame.draw.circle(screen, (0, 255, 0), (int(f['posX']), int(f['posY'])), 3)
        
        for p in predators:
            pygame.draw.circle(screen, (255, 50, 50), (int(p['posX']), int(p['posY'])), 8)
            pygame.draw.circle(screen, (150, 0, 0), (int(p['posX']), int(p['posY'])), 8, 2)

        pygame.display.set_caption(f"Gen: {generation} | Time: {GEN_DURATION - frameCount}")

        pygame.display.flip()
        clock.tick(60)
        
        frameCount += 1
        aliveCount = np.sum(agents['isActive'])

        foodRemaining = np.sum(food['isEaten'] < 0.5)

        if frameCount >= GEN_DURATION or aliveCount == 0 or foodRemaining == 0:
            reason = 'Time' if frameCount >= GEN_DURATION else 'Food Cleared' if foodRemaining == 0 else 'Extinction'          
            
            sortedIndices = np.argsort(agents['fitnessScore'])[::-1]
            bestScore = agents[sortedIndices[0]]['fitnessScore']            
            
            survivorCount = int(numAgents * 0.1) 
            worstSurvivorScore = agents[sortedIndices[survivorCount-1]]['fitnessScore']
            
            logMessage = f"Generation: {generation: <3} | Reason: {reason: <12} | Best Fitness Score: {bestScore: <4.1f} | Worst Survivor Score: {worstSurvivorScore: <4.1f}"
            
            with open("simulation_log.txt", "a") as f:
                f.write(logMessage + "\n")
            
            bestAgent = agents[sortedIndices[0]]
            saveBestBrain(bestAgent, "best_brain.npy")

            agents = evolveGeneration(agents, mutationRate=0.20)

            for a in agents:
                a['posX'] = np.random.uniform(100, 700)
                a['posY'] = np.random.uniform(100, 500)
                a['rotationAngle'] = np.random.uniform(0, 2 * np.pi)

            for f in food:
                f['posX'] = np.random.uniform(50, 750)
                f['posY'] = np.random.uniform(50, 550)
                f['isEaten'] = 0.0
                  
            generation += 1
            frameCount = 0
            print(f"--- G E N E R A T I O N     {generation} ---")

    pygame.quit()

if __name__ == "__main__":
    runSimulation()