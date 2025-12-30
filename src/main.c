#include "include/simulation.h"
#include <math.h>

void updateSimulation(Agent* agents, int agentCount, Food* foodBits, int foodCount, Predator* predators, int predCount, float deltaTime) {

    for (int i = 0; i < agentCount; i++) {
        Agent* agent = &agents[i];
        
        if (agent->isActive < 0.5f) continue;

        float senseLeft   = getSensorOutput(agent, foodBits, foodCount, -0.45f);
        float senseCenter = getSensorOutput(agent, foodBits, foodCount,  0.00f);
        float senseRight  = getSensorOutput(agent, foodBits, foodCount,  0.45f);

        float brainInputs[5] = {
            senseLeft, 
            senseCenter, 
            senseRight, 
            0.0f,
            0.0f
        };

        computeBrain(agent, brainInputs);

        agent->posX += cosf(agent->rotationAngle) * agent->velocity * deltaTime;
        agent->posY += sinf(agent->rotationAngle) * agent->velocity * deltaTime;

        if (agent->posX < 0.0f) agent->posX = 800.0f;
        if (agent->posX > 800.0f) agent->posX = 0.0f;
        if (agent->posY < 0.0f) agent->posY = 600.0f;
        if (agent->posY > 600.0f) agent->posY = 0.0f;

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
    
    for (int i = 0; i < predCount; i++) {
        Predator* p = &predators[i];
        
        float nearestDist = 10000.0f;
        Agent* target = NULL;

        for (int j = 0; j < agentCount; j++) {
            if (agents[j].isActive > 0.5f) {
                float dist = calculateDistance(p->posX, p->posY, agents[j].posX, agents[j].posY);
                if (dist < nearestDist) {
                    nearestDist = dist;
                    target = &agents[j];
                }
            }
        }

        if (target != NULL) {
            float dx = target->posX - p->posX;
            float dy = target->posY - p->posY;
            float angle = atan2f(dy, dx);

            p->velocity = 2.5f; 
            
            p->posX += cosf(angle) * p->velocity * deltaTime;
            p->posY += sinf(angle) * p->velocity * deltaTime;

            if (p->posX < 0.0f) p->posX = 800.0f;
            if (p->posX > 800.0f) p->posX = 0.0f;
            if (p->posY < 0.0f) p->posY = 600.0f;
            if (p->posY > 600.0f) p->posY = 0.0f;

            if (nearestDist < 10.0f) {
                target->isActive = 0.0f;
                target->fitnessScore -= 5.0f;
            }
        }
    }
}