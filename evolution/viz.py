import pygame
import numpy as np
import ctypes
from evolution.bridge import AgentStruct, FoodStruct, PredatorStruct, simulationLib, BRAIN_SIZE
from evolution.manager import evolveGeneration, saveBestBrain, loadBestBrain, mutate

def runSimulation():

    with open("simulation_log.txt", "w") as f:
        # Optional: Write a header row for easier reading later
        f.write("Generation:     | Reason:              | Best Fitness Score:      | Worst Survivor Score:     \n")
        f.write("-" * 93 + "\n")

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # --- SETUP ---
    numAgents = 50
    numFood = 120
    
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
        
        # FIX: Check if brain exists AND if the size matches the current BRAIN_SIZE
        if savedBrain is not None and savedBrain.shape[0] == BRAIN_SIZE:
            # OPTION A: Load the Genius
            a['brainWeights'] = savedBrain.copy()
            
            # Apply mutation (skip for the first one to keep a pure copy)
            if a is not agents[0]: 
                 noise = np.random.uniform(-0.1, 0.1, size=BRAIN_SIZE)
                 a['brainWeights'] += noise
        else:
            # OPTION B: Start Fresh (Random)
            # This runs if no file exists OR if the file size is wrong
            randomWeights = np.random.uniform(-1.0, 1.0, size=BRAIN_SIZE)
            for i in range(BRAIN_SIZE):
                a['brainWeights'][i] = randomWeights[i]

    # Initialize Food
    for f in food:
        f['posX'] = np.random.uniform(50, 750)
        f['posY'] = np.random.uniform(50, 550)
        f['isEaten'] = 0.0
    
    numPredators = 3 # Start with 3 hunters
    predators = np.zeros(numPredators, dtype=PredatorStruct)
    
    for p in predators:
        p['posX'] = np.random.uniform(0, 800)
        p['posY'] = np.random.uniform(0, 600)
        p['velocity'] = 2.0

    # --- GENERATION LOOP ---
    generation = 1
    frameCount = 0
    GEN_DURATION = 60 * 15 # 15 seconds per generation
    
    print(f"--- G E N E R A T I O N     {generation} ---")

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
            predators.ctypes.data_as(ctypes.POINTER(PredatorStruct)), # NEW ARG
            numPredators, # NEW ARG
            0.5 # deltaTime
        )

        # 3. Render
        screen.fill((20, 20, 20))

        # Draw Agents (White triangles)
        kingIndex = -1
        highestScore = -1.0
        
        for i in range(numAgents):
            if agents[i]['isActive'] > 0.5:
                if agents[i]['fitnessScore'] > highestScore:
                    highestScore = agents[i]['fitnessScore']
                    kingIndex = i

        # --- 3b. Draw Agents ---
        for i in range(numAgents):
            a = agents[i]
            if a['isActive'] > 0.5:
                # Default appearance (Standard Agent)
                color = (200, 200, 200) # Grey/White
                radius = 4
                thickness = 1
                
                # IS THIS THE KING?
                if i == kingIndex:
                    color = (255, 215, 0) # GOLD
                    radius = 6            # Larger
                    thickness = 0         # Filled circle
                    
                    # Optional: Draw a "Halo" around the king
                    pygame.draw.circle(screen, (255, 255, 0), (int(a['posX']), int(a['posY'])), 10, 1)

                # Calculate nose position for direction
                noseX = a['posX'] + np.cos(a['rotationAngle']) * 10
                noseY = a['posY'] + np.sin(a['rotationAngle']) * 10
                
                startPos = (int(a['posX']), int(a['posY']))
                endPos = (int(noseX), int(noseY))
                
                # Draw the Agent
                pygame.draw.line(screen, color, startPos, endPos, 2)
                pygame.draw.circle(screen, color, startPos, radius, thickness)

        # Draw Food (Green dots)
        for f in food:
            if f['isEaten'] < 0.5:
                pygame.draw.circle(screen, (0, 255, 0), (int(f['posX']), int(f['posY'])), 3)
        
        # Draw Predators (Red hexagons)
        for p in predators:
            pygame.draw.circle(screen, (255, 50, 50), (int(p['posX']), int(p['posY'])), 8)
            # Optional: Draw a ring to look scary
            pygame.draw.circle(screen, (150, 0, 0), (int(p['posX']), int(p['posY'])), 8, 2)

        # Draw Info Text
        pygame.display.set_caption(f"Gen: {generation} | Time: {GEN_DURATION - frameCount}")

        pygame.display.flip()
        clock.tick(60)

        # 4. Check for End of Generation
        frameCount += 1
        aliveCount = np.sum(agents['isActive'])

        foodRemaining = np.sum(food['isEaten'] < 0.5)

        if frameCount >= GEN_DURATION or aliveCount == 0 or foodRemaining == 0:
            reason = 'Time' if frameCount >= GEN_DURATION else 'Food Cleared' if foodRemaining == 0 else 'Extinction'
            
            # Sort to find stats
            sortedIndices = np.argsort(agents['fitnessScore'])[::-1]
            bestScore = agents[sortedIndices[0]]['fitnessScore']
            
            # Calculate the worst score among the survivors (top 10%)
            survivorCount = int(numAgents * 0.1) # Assuming 10% survival rate
            worstSurvivorScore = agents[sortedIndices[survivorCount-1]]['fitnessScore']

            # Construct the log message
            logMessage = f"Generation: {generation: <3} | Reason: {reason: <12} | Best Fitness Score: {bestScore: <4.1f} | Worst Survivor Score: {worstSurvivorScore: <4.1f}"
            
            # 1. Print to Console
            #print(logMessage)
            
            # 2. Save to File (Appends to the end of the file)
            with open("simulation_log.txt", "a") as f:
                f.write(logMessage + "\n")
            
            # 2. Save the winner
            bestAgent = agents[sortedIndices[0]]
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
            print(f"--- G E N E R A T I O N     {generation} ---")

    pygame.quit()

if __name__ == "__main__":
    runSimulation()