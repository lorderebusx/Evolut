#include "../include/simulation.h"
#include <math.h>

// Activation function: helps the brain handle non-linear decisions
float fastActivation(float x) {
    return (x > 0) ? x : 0; // ReLU
}

void computeBrain(Agent* agent, float* inputs) {
    float hiddenLayer[8];
    int currentWeight = 0;

    // 1. Calculate Hidden Layer
    for (int i = 0; i < 8; i++) {
        float sum = 0.0f;
        for (int j = 0; j < 5; j++) {
            sum += inputs[j] * agent->brainWeights[currentWeight++];
        }
        hiddenLayer[i] = fastActivation(sum);
    }

    // 2. Calculate Output Layer (2 Outputs)
    float outputLayer[2] = {0.0f, 0.0f};
    for (int i = 0; i < 2; i++) {
        float sum = 0.0f;
        for (int j = 0; j < 8; j++) {
            sum += hiddenLayer[j] * agent->brainWeights[currentWeight++];
        }
        outputLayer[i] = sum; // Raw output for steering/speed
    }

    // 3. Apply the "Decisions" to the agent
    // Output 0 controls steering (-0.1 to 0.1 radians)
    agent->rotationAngle += (tanf(outputLayer[0]) * 0.1f);
    
    // Output 1 controls speed (mapped to 0.0 - 5.0 range)
    agent->velocity = 1.0f + fastActivation(outputLayer[1]);
}