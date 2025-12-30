#include "../include/simulation.h"
#include <math.h>


float fastActivation(float x) {
    return (x > 0) ? x : 0; 
}

void computeBrain(Agent* agent, float* inputs) {
    float hiddenLayer[8];
    int currentWeight = 0;

    for (int i = 0; i < 8; i++) {
        float sum = 0.0f;
        for (int j = 0; j < 5; j++) {
            sum += inputs[j] * agent->brainWeights[currentWeight++];
        }
        hiddenLayer[i] = fastActivation(sum);
    }
    
    float outputLayer[2] = {0.0f, 0.0f};
    for (int i = 0; i < 2; i++) {
        float sum = 0.0f;
        for (int j = 0; j < 8; j++) {
            sum += hiddenLayer[j] * agent->brainWeights[currentWeight++];
        }
        outputLayer[i] = sum; 
    }

    agent->rotationAngle += (tanhf(outputLayer[0]) * 0.1f);
    agent->velocity = 2.5f + fastActivation(outputLayer[1]);
}