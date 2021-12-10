import numpy as np

class HungryStudent:
    def __init__(self, q, number):
        self.number = number
        self.time_queue = 0
        self.time_checkout = 0
        self.time_ate = 0
        self.L_queue = 0
        self.L_checkout = 0
        self.L_canteen = 0
        self.count_dishes = 2 if np.random.random() < q else 1
