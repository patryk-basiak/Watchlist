import random


def normalize_vector(vector):
    distance = sum(x ** 2 for x in vector)**0.5
    if distance == 0:
        return [0 for _ in vector]
    return [x / distance for x in vector]


class Perceptron:
    def __init__(self, alpha, dim, correct_path):
        self.alpha = alpha
        self.language = correct_path
        self.weights = [0 for _ in range(dim)]
        self.threshold = 1

    def learn(self, inputs, error):
        n_inputs = normalize_vector(inputs)
        for w in range(len(self.weights)):
            self.weights[w] += float(n_inputs[w]) * self.alpha * error
        self.weights = normalize_vector(self.weights)
        return error

    def compute(self, inputs):
        inputs = normalize_vector(inputs)
        if len(inputs) != len(self.weights):
            raise ValueError("Inputs size is not equal to weights size")
        value = 0
        for x in range(len(inputs)):
            value += float(inputs[x]) * self.weights[x]
        return value