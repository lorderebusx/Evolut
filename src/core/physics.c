#include "../include/simulation.h"
#include <math.h>

float calculateDistance(float x1, float y1, float x2, float y2) {
    float dx = x2 - x1;
    float dy = y2 - y1;
    return sqrtf(dx * dx + dy * dy);
}


float getSensorOutput(Agent* agent, Food* foodBits, int foodCount, float sensorAngleOffset) {
    float totalViewAngle = agent->rotationAngle + sensorAngleOffset;
    float bestDetection = 0.0f;
    float maxViewDistance = 200.0f; 

    for (int i = 0; i < foodCount; i++) {
        if (foodBits[i].isEaten > 0.5f) continue; 

        float dist = calculateDistance(agent->posX, agent->posY, foodBits[i].posX, foodBits[i].posY);
        
        if (dist < maxViewDistance) {
            
            float angleToFood = atan2f(foodBits[i].posY - agent->posY, foodBits[i].posX - agent->posX);
            
            
            float angleDiff = fabsf(totalViewAngle - angleToFood);
            if (angleDiff < 0.2f) {
                
                float detectionStrength = 1.0f - (dist / maxViewDistance);
                if (detectionStrength > bestDetection) {
                    bestDetection = detectionStrength;
                }
            }
        }
    }
    return bestDetection;
}