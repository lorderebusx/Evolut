#include "include/simulation.h"
#include <math.h>  // Added for cosf and sinf

void updateSimulation(Agent* agents, int agentCount, Food* foodBits, int foodCount, float deltaTime) {
    for (int i = 0; i < agentCount; i++) {
        Agent* agent = &agents[i];
        if (agent->isActive < 0.5f) continue;

        // The compiler now knows these functions exist because of simulation.h
        float senseLeft   = getSensorOutput(agent, foodBits, foodCount, -0.45f);
        float senseCenter = getSensorOutput(agent, foodBits, foodCount,  0.00f);
        float senseRight  = getSensorOutput(agent, foodBits, foodCount,  0.45f);

        // Prepare the 5 inputs for the brain
        float brainInputs[5] = {
            senseLeft, 
            senseCenter, 
            senseRight, 
            agent->energyLevel / 100.0f, // Normalized energy
            agent->velocity / 5.0f       // Normalized velocity
        };

        // Let the C-based neural network decide the movement
        computeBrain(agent, brainInputs);

        agent->posX += cosf(agent->rotationAngle) * agent->velocity * deltaTime;
        agent->posY += sinf(agent->rotationAngle) * agent->velocity * deltaTime;

        for (int j = 0; j < foodCount; j++) {
            if (foodBits[j].isEaten < 0.5f) {
                float dist = calculateDistance(agent->posX, agent->posY, foodBits[j].posX, foodBits[j].posY);
                if (dist < 10.0f) {
                    foodBits[j].isEaten = 1.0f;
                    agent->energyLevel += 20.0f;
                    agent->fitnessScore += 1.0f;
                }
            }
        }
        
        agent->energyLevel -= 0.05f * deltaTime;
        if (agent->energyLevel <= 0) agent->isActive = 0.0f;
    }
}