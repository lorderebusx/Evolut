import pygame
import numpy as np
import ctypes
from evolution.bridge import AgentStruct, FoodStruct, simulationLib, BRAIN_SIZE
from evolution.manager import evolveGeneration, saveBestBrain, loadBestBrain, mutate

def runSimulation():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # --- SETUP ---
    numAgents = 50
    numFood = 80
    
    agents = np.zeros(numAgents, dtype=AgentStruct)
    food = np.zeros(numFood, dtype=FoodStruct)

    # Initial Random Setup
    # ... inside runSimulation() ...
    
    # Import the new functions
    from evolution.manager import evolveGeneration, saveBestBrain, loadBestBrain

    # Try to load a saved brain
    savedBrain = loadBestBrain("best_brain.npy")

    # Initialize Agents
    for a in agents:
        a['isActive'] = 1.0
        a['energyLevel'] = 100.0
        a['posX'] = np.random.uniform(100, 700)
        a['posY'] = np.random.uniform(100, 500)
        a['rotationAngle'] = np.random.uniform(0, 2 * np.pi)
        
        if savedBrain is not None:
            # OPTION A: Load the Genius
            # We give the saved brain to the agent, but MUTATE it slightly
            # so we don't have 50 identical robots stacking on top of each other.
            a['brainWeights'] = savedBrain.copy()
            
            # Apply a tiny mutation to create diversity around the "Master" strategy
            # (Skip mutation for the very first agent so we keep one pure copy)
            if a is not agents[0]: 
                 # Assuming mutate is available (we might need to import it or move it)
                 # For now, let's just do a quick manual noise add
                 noise = np.random.uniform(-0.1, 0.1, size=BRAIN_SIZE)
                 a['brainWeights'] += noise
        else:
            # OPTION B: Start Fresh (Random)
            randomWeights = np.random.uniform(-1.0, 1.0, size=BRAIN_SIZE)
            for i in range(BRAIN_SIZE):
                a['brainWeights'][i] = randomWeights[i]

    # Initialize Food
        for f in food:
            f['posX'] = np.random.uniform(50, 750)
            f['posY'] = np.random.uniform(50, 550)
            f['isEaten'] = 0.0

    # --- GENERATION LOOP ---
    generation = 1
    frameCount = 0
    GEN_DURATION = 60 * 30 # 15 seconds per generation
    
    print(f"--- STARTING GEN {generation} ---")

    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # 2. Update C Engine
        simulationLib.updateSimulation(
            agents.ctypes.data_as(ctypes.POINTER(AgentStruct)),
            numAgents,
            food.ctypes.data_as(ctypes.POINTER(FoodStruct)),
            numFood,
            0.5 # Time step
        )

        # 3. Render
        screen.fill((20, 20, 20))

        # Draw Agents (White triangles)
        for a in agents:
            if a['isActive'] > 0.5:
                # Calculate nose position for direction
                noseX = a['posX'] + np.cos(a['rotationAngle']) * 10
                noseY = a['posY'] + np.sin(a['rotationAngle']) * 10
                
                # FIX: Cast everything to int() for Pygame
                startPos = (int(a['posX']), int(a['posY']))
                endPos = (int(noseX), int(noseY))
                
                pygame.draw.line(screen, (255, 255, 255), startPos, endPos, 2)
                pygame.draw.circle(screen, (200, 200, 200), startPos, 4)

        # Draw Food (Green dots)
        for f in food:
            if f['isEaten'] < 0.5:
                pygame.draw.circle(screen, (0, 255, 0), (int(f['posX']), int(f['posY'])), 3)

        # Draw Info Text
        pygame.display.set_caption(f"Gen: {generation} | Time: {GEN_DURATION - frameCount}")

        pygame.display.flip()
        clock.tick(60)

        # 4. Check for End of Generation
        frameCount += 1
        aliveCount = np.sum(agents['isActive'])

        foodRemaining = np.sum(food['isEaten'] < 0.5)

        if frameCount >= GEN_DURATION or aliveCount == 0 or foodRemaining == 0:
            print(f"Gen Complete! (Reason: {'Time' if frameCount >= GEN_DURATION else 'Food Cleared' if foodRemaining == 0 else 'Extinction'})")
            
            sortedIndices = np.argsort(agents['fitnessScore'])[::-1]
            bestAgent = agents[sortedIndices[0]]
            
            # 2. Save the winner
            saveBestBrain(bestAgent, "best_brain.npy")
            
            # 3. Evolve the population (this overwrites the array)
            agents = evolveGeneration(agents, mutationRate=0.20)
            
            # Reset World
            for a in agents:
                a['posX'] = np.random.uniform(100, 700)
                a['posY'] = np.random.uniform(100, 500)
                a['rotationAngle'] = np.random.uniform(0, 2 * np.pi)
            
            # Respawn Food
            for f in food:
                f['posX'] = np.random.uniform(50, 750)
                f['posY'] = np.random.uniform(50, 550)
                f['isEaten'] = 0.0
                
            generation += 1
            frameCount = 0
            print(f"--- STARTING GEN {generation} ---")

    pygame.quit()

if __name__ == "__main__":
    runSimulation()