import pygame
import numpy as np
import ctypes
from evolution.bridge import AgentStruct, FoodStruct, simulationLib, BRAIN_SIZE
from evolution.manager import evolveGeneration

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
    for a in agents:
        a['isActive'] = 1.0
        a['energyLevel'] = 100.0
        a['posX'] = np.random.uniform(100, 700)
        a['posY'] = np.random.uniform(100, 500)
        a['rotationAngle'] = np.random.uniform(0, 2 * np.pi)
        
        # Random brains for Gen 0
        randomWeights = np.random.uniform(-1.0, 1.0, size=BRAIN_SIZE)
        for i in range(BRAIN_SIZE):
            a['brainWeights'][i] = randomWeights[i]

    for f in food:
        f['posX'] = np.random.uniform(50, 750)
        f['posY'] = np.random.uniform(50, 550)
        f['isEaten'] = 0.0

    # --- GENERATION LOOP ---
    generation = 1
    frameCount = 0
    GEN_DURATION = 60 * 15 # 15 seconds per generation
    
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

        # Draw Food (Green dots)
        for f in food:
            if f['isEaten'] < 0.5:
                pygame.draw.circle(screen, (0, 200, 100), (int(f['posX']), int(f['posY'])), 4)

        # Draw Agents (White triangles)
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

        # Draw Info Text
        pygame.display.set_caption(f"Gen: {generation} | Time: {GEN_DURATION - frameCount}")

        pygame.display.flip()
        clock.tick(60)

        # 4. Check for End of Generation
        frameCount += 1
        aliveCount = np.sum(agents['isActive'])

        if frameCount >= GEN_DURATION or aliveCount == 0:
            print("Evolution running...")
            
            # EVOLVE!
            agents = evolveGeneration(agents)
            
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