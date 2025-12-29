#include "include/simulation.h"
#include <math.h>

// FIX: Updated signature to accept Predator arguments
void updateSimulation(Agent* agents, int agentCount, Food* foodBits, int foodCount, Predator* predators, int predCount, float deltaTime) {
    
    // --- PART 1: UPDATE AGENTS ---
    for (int i = 0; i < agentCount; i++) {
        Agent* agent = &agents[i];
        
        // Skip dead agents
        if (agent->isActive < 0.5f) continue;

        // Sensors
        float senseLeft   = getSensorOutput(agent, foodBits, foodCount, -0.45f);
        float senseCenter = getSensorOutput(agent, foodBits, foodCount,  0.00f);
        float senseRight  = getSensorOutput(agent, foodBits, foodCount,  0.45f);

        // Inputs (Zeroed out Energy/Velocity to fix spinning)
        float brainInputs[5] = {
            senseLeft, 
            senseCenter, 
            senseRight, 
            0.0f,
            0.0f
        };

        computeBrain(agent, brainInputs);

        // Movement
        agent->posX += cosf(agent->rotationAngle) * agent->velocity * deltaTime;
        agent->posY += sinf(agent->rotationAngle) * agent->velocity * deltaTime;

        // Agent Wrap-Around (Pac-Man)
        if (agent->posX < 0.0f) agent->posX = 800.0f;
        if (agent->posX > 800.0f) agent->posX = 0.0f;
        if (agent->posY < 0.0f) agent->posY = 600.0f;
        if (agent->posY > 600.0f) agent->posY = 0.0f;

        // Eating Food
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
        
        // Energy Decay
        agent->energyLevel -= 0.05f * deltaTime;
        if (agent->energyLevel <= 0) agent->isActive = 0.0f;
    } // <--- END OF AGENT LOOP

    // --- PART 2: UPDATE PREDATORS (Completely separate loop) ---
    for (int i = 0; i < predCount; i++) {
        Predator* p = &predators[i];
        
        float nearestDist = 10000.0f;
        Agent* target = NULL;

        // Find nearest tasty Agent
        for (int j = 0; j < agentCount; j++) {
            if (agents[j].isActive > 0.5f) {
                float dist = calculateDistance(p->posX, p->posY, agents[j].posX, agents[j].posY);
                if (dist < nearestDist) {
                    nearestDist = dist;
                    target = &agents[j];
                }
            }
        }

        // Move towards target
        if (target != NULL) {
            float dx = target->posX - p->posX;
            float dy = target->posY - p->posY;
            float angle = atan2f(dy, dx); // Point at the agent
            
            // Predators move at constant speed
            p->velocity = 2.5f; 
            
            p->posX += cosf(angle) * p->velocity * deltaTime;
            p->posY += sinf(angle) * p->velocity * deltaTime;

            // FIX: Predator Wrap-Around (So they don't get stuck at walls)
            if (p->posX < 0.0f) p->posX = 800.0f;
            if (p->posX > 800.0f) p->posX = 0.0f;
            if (p->posY < 0.0f) p->posY = 600.0f;
            if (p->posY > 600.0f) p->posY = 0.0f;

            // Kill Logic
            if (nearestDist < 10.0f) {
                target->isActive = 0.0f; // Agent dies
                target->fitnessScore -= 5.0f; // Penalty for getting eaten
            }
        }
    } // <--- END OF PREDATOR LOOP
}