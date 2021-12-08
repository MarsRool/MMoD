import math
from functools import reduce
from tabulate import tabulate
import matplotlib.pyplot as plt

# Calculate Empirical Characteristics
def calculate_empirical_characteristics(qs):
    L_queuing_system_list, L_queue_list, t_queuing_system_list, t_queue_list = qs.get_results()
    p = []
    for i in range(qs.n + qs.m + 1):
        request_frequency = reduce( lambda count, x: count+1 if x == i else count, L_queuing_system_list, 0)
        p.append(request_frequency / len(L_queuing_system_list))
    p_reject = p[qs.n + qs.m]
    Q = 1 - p_reject
    A = qs.lambd * Q
    n_occuped = Q * qs.lambd / qs.mu
    L_queue = sum(L_queue_list) / len(L_queue_list)
    L_queuing_system = sum(L_queuing_system_list) / len(L_queuing_system_list)
    t_queuing_system = sum(t_queuing_system_list) / len(t_queuing_system_list)
    t_queue = sum(t_queue_list) / len(t_queue_list)

    return p, Q, A, p_reject, n_occuped, L_queuing_system, L_queue, t_queuing_system, t_queue


# Calculate Theoretical Characteristics
def calculate_theoretical_characteristics(n, m, lambd, mu, v):
    alpha = lambd / mu
    betta = v / mu 
    p=[]
    p_0 = (
                 sum([alpha ** i / math.factorial(i) for i in range (n+1)]) +
                 alpha ** n / math.factorial(n) *
                 sum([alpha ** i / reduce( 
                     lambda prod, x: prod * x, [ (n + l * betta) for l in range(1, i + 1) ] 
                 ) for i in range(1,m+1)])
           ) ** (-1)
    p.append(p_0)
    for k in range(1,n + 1):
        p_k = alpha ** k / math.factorial(k) * p[0]
        p.append(p_k)
    for i in range(1,m + 1):
        p_n_i = p[n] * alpha ** i / reduce( 
                     lambda prod, x: prod * x, [ (n + l * betta) for l in range(1,i + 1) ] 
                 )
        p.append(p_n_i)
    p_reject = p[n + m]
    Q = 1 - p_reject
    A = lambd * Q
    L_queue = sum([ i * p[n + i] for i in range(1,m + 1)])
    n_occuped = Q * lambd / mu
    L_queuing_system = sum([k * p[k] for k in range(1, n + 1)]) + sum([(n + i) * p[n + i] for i in range(1, m + 1)])
    t_queuing_system = L_queuing_system / lambd
    t_queue = L_queue / lambd

    return p, Q, A, p_reject, n_occuped, L_queuing_system, L_queue, t_queuing_system, t_queue


# Display Tabls Characteristics
def display_characteristics(theoretical_characteristics, empirical_characteristics):
    p1, Q1, A1, p_reject1, n_occuped1, L_queuing_system1, L_queue1, t_queuing_system1, t_queue1 = theoretical_characteristics
    p2, Q2, A2, p_reject2, n_occuped2, L_queuing_system2, L_queue2, t_queuing_system2, t_queue2 = empirical_characteristics

    output_list = [[f'p{(i)}', p1[i], p2[i]] for i in range (min(len(p1), 15))]
    output_list.extend([['Q (относительная пропускная способность)', Q1, Q2],
                        ['A (абсолютная пропускная способность)', A1, A2],
                        ['p отказа', p_reject1, p_reject2],
                        ['L СМО (среднее число заявок в СМО)', L_queuing_system1, L_queuing_system2],
                        ['L очереди (среднее число заявок в очереди)', L_queue1, L_queue2],
                        ['t СМО (среднее время заявки в СМО)', t_queuing_system1, t_queuing_system2],
                        ['t очереди (среднее время заявки в очереди)', t_queue1, t_queue2],
                        ['n занятости (среднее число занятых каналов)', n_occuped1, n_occuped2]])
    print(tabulate(output_list,
          headers=['', 'Теоретические характеристики', 'Эмпирические характеристики']))
    print()


def get_xi_2(o, e):
    return sum(((o[i] - e[i]) ** 2) / e[i] for i in range(len(o)))


def plot_graphs(theoretical_characteristic, empirical_characteristic):
    plt.plot(theoretical_characteristic[0])
    plt.plot(empirical_characteristic[0])
    plt.legend(['Теоретические вероятности', 'Эмпирические вероятности'])
    plt.xlabel('p[i]')
    plt.show()
