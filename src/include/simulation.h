#ifndef SIMULATION_H
#define SIMULATION_H

#include <stdint.h>

// FIX: Set Brain Size to 56 (Matches neural.c logic)
#define BRAIN_SIZE 56 

typedef struct {
    float isActive;      // 1
    float posX;          // 2
    float posY;          // 3
    float rotationAngle; // 4
    float energyLevel;   // 5
    float velocity;      // 6
    float brainWeights[BRAIN_SIZE]; // 7
    float fitnessScore;  // 8
} Agent;

typedef struct {
    float posX;
    float posY;
    float isEaten;
} Food;

typedef struct {
    float posX;
    float posY;
    float velocity;
} Predator;

// Function Prototypes
void updateSimulation(Agent* agents, int agentCount, Food* foodBits, int foodCount, Predator* predators, int predCount, float deltaTime);
float calculateDistance(float x1, float y1, float x2, float y2);
float getSensorOutput(Agent* agent, Food* foodBits, int foodCount, float sensorAngleOffset);
void computeBrain(Agent* agent, float* inputs);

#endif