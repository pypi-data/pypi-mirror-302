import numpy as np


def train(network, x, y, loss_func, epochs):
    for epoch in range(epochs):
        network.backward(x, y, loss_func)
        loss_value = loss_func(y, network.forward(x))
        print(f"Эпоха {epoch + 1}/{epochs}, Потеря: {loss_value:.4f}")
