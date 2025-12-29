#include "../include/simulation.h"
#include <math.h>

// Helper to calculate distance between two points
float calculateDistance(float x1, float y1, float x2, float y2) {
    float dx = x2 - x1;
    float dy = y2 - y1;
    return sqrtf(dx * dx + dy * dy);
}

// Simple sensor: returns 1.0 if food is within a cone of vision, 0.0 otherwise
float getSensorOutput(Agent* agent, Food* foodBits, int foodCount, float sensorAngleOffset) {
    float totalViewAngle = agent->rotationAngle + sensorAngleOffset;
    float bestDetection = 0.0f;
    float maxViewDistance = 200.0f; // How far the agent can see

    for (int i = 0; i < foodCount; i++) {
        if (foodBits[i].isEaten > 0.5f) continue; // Skip eaten food

        float dist = calculateDistance(agent->posX, agent->posY, foodBits[i].posX, foodBits[i].posY);
        
        if (dist < maxViewDistance) {
            // Calculate angle to the food
            float angleToFood = atan2f(foodBits[i].posY - agent->posY, foodBits[i].posX - agent->posX);
            
            // Check if the food is within a narrow "vision beam" (e.g., 0.2 radians)
            float angleDiff = fabsf(totalViewAngle - angleToFood);
            if (angleDiff < 0.2f) {
                // Return a value that is higher the closer the food is
                float detectionStrength = 1.0f - (dist / maxViewDistance);
                if (detectionStrength > bestDetection) {
                    bestDetection = detectionStrength;
                }
            }
        }
    }
    return bestDetection;
}