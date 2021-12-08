import simpy
import numpy as np
from functools import reduce
from tabulate import tabulate
import matplotlib.pyplot as plt

# Multichannel Queuing System Simulation processes class
class QueuingSystemSimulation:
    def __init__(self, n, m, lambd, mu, v, env):
        # queuing system params
        self.n = n
        self.m = m
        self.lambd = lambd
        self.mu = mu
        self.v = v
        # empirical values lists
        self.L_queuing_system_list = []
        self.L_queue_list = []
        self.t_queuing_system_list = []
        self.t_queue_list = []
        # enviromental variables for simpy simulation
        self.env = env
        self.loader = simpy.Resource(env, n)

    # Multichannel Queuing Simulation with parameters n, m, lambd, mu, v, test_time
    @staticmethod
    def simulate_queuing_system(n, m, lambd, mu, v, test_time):
        env = simpy.Environment()
        qs = QueuingSystemSimulation(n, m, lambd, mu, v, env)
        env.process(qs.run())
        env.run(until=test_time)
        return qs

    def run(self):
        while True:
            yield self.env.timeout(np.random.exponential(1/self.lambd))
            self.env.process(self.make_request())

    def make_request(self):
        queque_len_before = len(self.loader.queue)
        n_busy = self.loader.count

        with self.loader.request() as request:
            self.L_queue_list.append(queque_len_before)
            self.L_queuing_system_list.append(queque_len_before + n_busy)
            if len(self.loader.queue) <= self.m:
                arrival_time = self.env.now

                waiting_process = self.env.process(self.waiting_in_queue())
                result = yield request | waiting_process    

                self.t_queue_list.append(self.env.now - arrival_time)
                if request in result:
                    yield self.env.process(self.request_processing())
                    self.t_queuing_system_list.append(self.env.now - arrival_time)
                else:
                    self.t_queuing_system_list.append(self.env.now - arrival_time)
            else:
                self.t_queue_list.append(0)
                self.t_queuing_system_list.append(0)

    def request_processing(self):
        yield self.env.timeout(np.random.exponential(1/self.mu))

    def waiting_in_queue(self):
        yield self.env.timeout(np.random.exponential(1/self.v))

    def get_results(self):
        return self.L_queuing_system_list, self.L_queue_list, self.t_queuing_system_list, self.t_queue_list