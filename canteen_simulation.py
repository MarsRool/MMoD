import simpy
import numpy as np
from hungry_student import HungryStudent

# Singlechannel Canteen Simulation processes class
class CanteenSimulation:
    def __init__(self, X, mu, q, t, env):
        # queuing system params
        self.X = X
        self.mu = mu
        self.q = q
        self.t = t
        # empirical values lists:
        # 1) queue - students in the queue
        # 2) checkout - students in the queue and cash desk
        # 3) canteen - students in the queue, cash desk and overall canteen (while eating)
        self.L_canteen_list = []
        self.L_checkout_list = []
        self.L_queue_list = []
        self.t_canteen_list = []
        self.t_checkout_list = []
        self.t_queue_list = []
        self.hungry_students = []
        # enviromental variables for simpy simulation
        self.env = env
        self.checkout_performer = simpy.Resource(env)
        self.eating_performer = simpy.Resource(env, 5000)

    # Singlechannel Canteen Simulation with parameters X, mu, v, test_time
    @staticmethod
    def simulate_canteen(X, mu, q, t, test_time):
        env = simpy.Environment()
        canteen = CanteenSimulation(X, mu, q, t, env)
        env.process(canteen.process_hungry_students_queue())
        env.process(canteen.process_hungry_students())
        env.run(until=test_time)
        return canteen

    def process_hungry_students(self):
        while True:
            yield self.env.timeout(0.01)
            while len(self.hungry_students) != 0:
                hungry_student = self.hungry_students.pop(0)
                self.env.process(self.make_eat_request(hungry_student))

    def process_hungry_students_queue(self):
        students_counter = 1
        while True:
            yield self.env.timeout(np.random.exponential(1/self.X))
            hungry_student = HungryStudent(self.q, students_counter)
            students_counter = students_counter + 1
            self.env.process(self.make_queue_request(hungry_student))

    def make_eat_request(self, hungry_student):
        eating_count_before = self.eating_performer.count

        with self.eating_performer.request() as request:
            hungry_student.L_canteen = hungry_student.L_checkout + eating_count_before
            arrival_time = self.env.now
            # print(f'Student №{hungry_student.number} starts eating at {arrival_time}')
            # print(f'L_canteen: {hungry_student.L_canteen}')

            yield request
            for _ in range(hungry_student.count_dishes):
                yield self.env.process(self.request_eating())
            hungry_student.time_ate = hungry_student.time_checkout + self.env.now - arrival_time
            # print(f'Student №{hungry_student.number} finished eating at {self.env.now}; time_ate = {hungry_student.time_ate}')
            # print(hungry_student.L_canteen, hungry_student.L_checkout, hungry_student.L_queue,
            #       hungry_student.time_ate, hungry_student.time_checkout, hungry_student.time_queue)
            self.L_canteen_list.append(hungry_student.L_canteen)
            self.L_checkout_list.append(hungry_student.L_checkout)
            self.L_queue_list.append(hungry_student.L_queue)
            self.t_canteen_list.append(hungry_student.time_ate)
            self.t_checkout_list.append(hungry_student.time_checkout)
            self.t_queue_list.append(hungry_student.time_queue)

    def make_queue_request(self, hungry_student):
        queque_len_before = len(self.checkout_performer.queue)
        queque_count_before = self.checkout_performer.count

        with self.checkout_performer.request() as request:
            hungry_student.L_queue = queque_len_before
            hungry_student.L_checkout = queque_len_before + queque_count_before
            arrival_time = self.env.now
            # print(f'Student №{hungry_student.number} arrived at {arrival_time}')

            yield request
            hungry_student.time_queue = self.env.now - arrival_time
            # print(f'Student №{hungry_student.number} passed queue at {self.env.now}; time_queue = {hungry_student.time_queue}')

            for _ in range(hungry_student.count_dishes):
                yield self.env.process(self.request_checkout_processing())
            hungry_student.time_checkout = self.env.now - arrival_time
            self.hungry_students.append(hungry_student)
            # print(f'Student №{hungry_student.number} passed cash desk at {self.env.now}; time_checkout = {hungry_student.time_checkout}')
            # print(f'Hungry Students count {len(self.hungry_students)}')

    def request_eating(self):
        yield self.env.timeout(np.random.exponential(self.t))

    def request_checkout_processing(self):
        yield self.env.timeout(np.random.exponential(1/self.mu))

    def get_results(self):
        return self.L_canteen_list, self.L_queue_list, self.t_canteen_list, self.t_queue_list

# CanteenSimulation.simulate_canteen(X = 2, mu = 5, q = 0.0, t = 1, test_time = 20)
