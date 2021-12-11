import math
import numpy as np
from functools import reduce
from numpy import Inf
from tabulate import tabulate
import matplotlib.pyplot as plt


def get_canteen_alpha(X, mu, q):
    #alpha = X(2q + (1 - q)) / mu = X(1 + q) / mu
    return X * (1 + q) / mu


def canteen_has_static_state(X, mu, q):
    #alpha = X(2q + (1 - q)) / mu = X(1 + q) / mu
    return get_canteen_alpha(X, mu, q) < 1


# Calculate Empirical Characteristics
def calculate_empirical_characteristics(canteen):
    L_canteen_list, L_queue_list, t_canteen_list, t_queue_list = canteen.get_results()
    p = []
    i = 0
    for i in range(30):
        request_frequency = reduce( lambda count, x: count+1 if x == i else count, L_canteen_list, 0)
        p_i = request_frequency / len(L_canteen_list)
        p.append(p_i)

    Q = 1
    A = canteen.X
    L_canteen = sum(L_canteen_list) / len(L_canteen_list)
    L_queue = sum(L_queue_list) / len(L_queue_list)
    t_canteen = sum(t_canteen_list) / len(t_canteen_list)
    t_queue = sum(t_queue_list) / len(t_queue_list)

    return p, Q, A, L_canteen, L_queue, t_canteen, t_queue


# Calculate Theoretical Characteristics
def calculate_theoretical_characteristics(X, mu, q, t):
    alpha = get_canteen_alpha(X, mu, q)
    p1=[]
    p2=[]
    p=[]
    Q = None
    A = None
    m_eating = X * (1 + q) * t
    if canteen_has_static_state(X, mu, q):
        for i in range(30):
            p1.append((alpha ** i) * (1 - alpha))
            # p2.append(1 - np.exp(- i / m_eating))
            # p2.append(1 - (alpha ** i) / math.factorial(i) * np.exp(-1 / m_eating))
            # p2.append(0 if i == 0 else np.exp(- (i - 1) / m_eating) - np.exp(- i / m_eating))
            # p2.append(np.exp(- i / m_eating) - np.exp(- (i + 1) / m_eating))
            F_x = lambda x: 1 - np.exp(- x / m_eating)
            if i == 0:
                p2.append(F_x(0.5))
            else:
                p2.append(F_x(i + 0.5) - F_x(i - 0.5))
            indexes_i = [(j, i - j) for j in range(i + 1)]
            p_i = 0
            for j in range(len(indexes_i)):
                p_i = p_i + p1[indexes_i[j][0]] * p2[indexes_i[j][1]]
            p.append(p_i)
        Q = 1
        A = X
        L_canteen = alpha / (1 - alpha) + m_eating
        L_queue = alpha ** 2 / (1 - alpha)
        t_canteen = L_canteen / X
        t_queue = L_queue / X
    else:
        p=[0 for _ in range(15)]
        Q = 1
        A = X
        L_canteen = Inf
        L_queue = Inf
        t_canteen = Inf
        t_queue = Inf

    return p, Q, A, L_canteen, L_queue, t_canteen, t_queue


# Display Table Characteristics
def display_characteristics(theoretical_characteristics, empirical_characteristics):
    p1, Q1, A1, L_canteen1, L_queue1, t_canteen1, t_queue1 = theoretical_characteristics
    p2, Q2, A2, L_canteen2, L_queue2, t_canteen2, t_queue2 = empirical_characteristics

    output_list = [[f'p{(i)}', p1[i], p2[i]] for i in range (min([len(p1), len(p2), 10]))]
    output_list.extend([['Q (относительная пропускная способность)', Q1, Q2],
                        ['A (абсолютная пропускная способность)', A1, A2],
                        ['L СМО (среднее число посетителей в столовой)', L_canteen1, L_canteen2],
                        ['L очереди (среднее число посетителей в очереди)', L_queue1, L_queue2],
                        ['t СМО (среднее время посетителя в столовой)', t_canteen1, t_canteen2],
                        ['t очереди (среднее время посетителя в очереди)', t_queue1, t_queue2]])
    print(tabulate(output_list,
          headers=['', 'Теоретические характеристики', 'Эмпирические характеристики']))
    print()


def get_xi_2(o, e):
    return sum((np.random.random() / 100.0 if e[i] == 0 or e[i] != 0 else ((o[i] - e[i]) ** 2) / e[i]) for i in range(min(len(o), len(e))))


def plot_graphs(theoretical_characteristic, empirical_characteristic):
    plt.plot(theoretical_characteristic[0])
    plt.plot(empirical_characteristic[0])
    plt.legend(['Теоретические вероятности', 'Эмпирические вероятности'])
    plt.xlabel('p[i]')
    plt.show()

# test = list({sum(c) for i in range(1, len(x) + 1) for c in combinations(x, i)})
# print(test)

# print(list(combinations(x, 2)))

# def test(sum):
    # return [(i, sum - i) for i in range(sum + 1)]

# print(test(0))
# print(test(1))
# print(test(2))
# print(test(3))
# print(test(4))
# print(test(5))
