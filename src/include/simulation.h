#ifndef SIMULATION_H
#define SIMULATION_H

#include <stdint.h>

#define BRAIN_SIZE 66

typedef struct {
    float isActive;
    float energyLevel;
    float fitnessScore;
    float posX;
    float posY;
    float rotationAngle;
    float velocity;
    float brainWeights[BRAIN_SIZE];
} Agent;

typedef struct {
    float posX;
    float posY;
    float isEaten;
} Food;

// --- Function Prototypes (The Fix) ---
void updateSimulation(Agent* agents, int agentCount, Food* foodBits, int foodCount, float deltaTime);
float calculateDistance(float x1, float y1, float x2, float y2);
float getSensorOutput(Agent* agent, Food* foodBits, int foodCount, float sensorAngleOffset);
void computeBrain(Agent* agent, float* inputs);

#endif