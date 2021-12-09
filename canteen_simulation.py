import simpy
import numpy as np

# Singlechannel Canteen Simulation processes class
class CanteenSimulation:
    def __init__(self, X, mu, q, t, env):
        # queuing system params
        self.X = X
        self.mu = mu
        self.q = q
        self.t = t
        # empirical values lists
        self.L_canteen_system_list = []
        self.L_queue_list = []
        self.t_canteen_system_list = []
        self.t_queue_list = []
        # enviromental variables for simpy simulation
        self.env = env
        self.loader = simpy.Resource(env)

    # Singlechannel Canteen Simulation with parameters X, mu, v, test_time
    @staticmethod
    def simulate_canteen(X, mu, q, t, test_time):
        env = simpy.Environment()
        qs = CanteenSimulation(X, mu, q, t, env)
        env.process(qs.run())
        env.run(until=test_time)
        return qs

    def run(self):
        while True:
            yield self.env.timeout(np.random.exponential(1/self.X))
            self.env.process(self.make_request())

    def make_request(self):
        queque_len_before = len(self.loader.queue)
        n_busy = self.loader.count

        with self.loader.request() as request:
            self.L_queue_list.append(queque_len_before)
            self.L_canteen_system_list.append(queque_len_before + n_busy)
            arrival_time = self.env.now

            yield request
            self.t_queue_list.append(self.env.now - arrival_time)

            if np.random.random() < self.q:
                yield self.env.process(self.request_processing())
            yield self.env.process(self.request_processing())
            self.t_canteen_system_list.append(self.env.now - arrival_time)

    def request_processing(self):
        yield self.env.timeout(np.random.exponential(1/self.mu))

    def get_results(self):
        return self.L_canteen_system_list, self.L_queue_list, self.t_canteen_system_list, self.t_queue_list
