import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np


#This method creates a connected graph and returns it
def create_connected_graph (n, p, w):
    is_graph_connected = False
    while not is_graph_connected:
        er = nx.erdos_renyi_graph(n, p)
        is_graph_connected = nx.is_connected(er)
    for u,v,d in er.edges(data=True):
        d['weight'] = random.randint(1, w)
    return er

#This method returns a list of sorted edges by their weight
def sort_edges(er):
    sorted_edges = sorted(er.edges(data=True), key=lambda t: t[2].get('weight', 1))
    return sorted_edges

#This method returns graph H with the same nodes as graph G ( er ) and uses dijkstra to decide which of G edges should occure in H graph too
def build_h(er, sorted_edges, r):
    graph_h = nx.Graph()
    graph_h.add_nodes_from(er.nodes(data = True))
    for u, v, d in sorted_edges:
        if(nx.has_path(graph_h, u, v)):
            shortest_path_weight = nx.dijkstra_path_length(graph_h, source= u, target= v,weight='weight')
        else:
            shortest_path_weight = float("inf")
        if r * d['weight'] < shortest_path_weight:
            graph_h.add_weighted_edges_from([(u, v, d['weight'])])
    return graph_h

#Main experiments method
def conduct_yours_experiment():
    n = input('Enter number of vertex: ')
    print "you entered: n = {} \n".format(n)
    p = input('Enter probability for an edge: ')
    print "you entered: p = {}\n".format(p)
    w = input('Enter max weight for an edge: ')
    print "you entered: w = {}\n".format(w)
    r = input('Enter stretch factor: ')
    print "you entered: r = {}\n".format(r)
    er = create_connected_graph(n, p, w)
    nx.draw(er)
    plt.savefig('graph_G.png')
    plt.gcf().clear()
    sorted_edges = sort_edges(er)
    print "original graph: {}".format(er.edges(data='weight'))
    new_h = build_h(er, sorted_edges, r)
    print "graph H: {}".format(new_h.edges(data='weight'))
    nx.draw(new_h)
    plt.savefig('graph_H.png')
    plt.gcf().clear()

def experiment_one():
    n = 100
    p = 0.5
    w = 1
    original_list = []
    r3_list = []
    r4_list = []
    r5_list = []
    r6_list = []
    # create 100 graphs
    for i in range(0, 100):
        er = create_connected_graph(n, p, w)
        original_list.append(er.number_of_edges())  # add number of edges
        sorted_edges = sort_edges(er)
      #  new_h2 = build_h(er, sorted_edges, 2)
      #  r2_list.append(new_h2.number_of_edges())    # add number of edges
        new_h3 = build_h(er, sorted_edges, 3)
        r3_list.append(new_h3.number_of_edges())    # add number of edges
        new_h4 = build_h(er, sorted_edges, 4)
        r4_list.append(new_h4.number_of_edges())    # add number of edges
        new_h5 = build_h(er, sorted_edges, 5)
        r5_list.append(new_h5.number_of_edges())    # add number of edges
        new_h6 = build_h(er, sorted_edges, 6)
        r6_list.append(new_h6.number_of_edges())    # add number of edges

    plt.plot(original_list, r3_list, marker='o', label="r=3")
    plt.plot(original_list, r4_list, marker='o', label="r=4")
    plt.plot(original_list, r5_list, marker='o', label="r=5")
    plt.plot(original_list, r6_list, marker='o', label="r=6")
    plt.xlabel('original graph - number of edges')
    plt.ylabel('spanner graph - number of edges')
    plt.title('experiment 1')
    plt.ylim(0,300)
    plt.legend()
    plt.show()


def experiment_two():
    n = 20
    p = 0.5
    w = 1
    original_list = []
    r1_list = []
    # create 100 graphs
    for i in range(0, 100):
        er = create_connected_graph(n, p, w)
        original_list.append(er.number_of_edges())  # add number of edges
        sorted_edges = sort_edges(er)
        new_h1 = build_h(er, sorted_edges, 1)
        r1_list.append(new_h1.number_of_edges())    # add number of edges

    plt.plot(original_list, r1_list, marker='o', label="r=1")
    plt.xlabel('original graph - number of edges')
    plt.ylabel('spanner graph - number of edges')
    plt.title('experiment 2')
    # plt.ylim(0,300)
    plt.legend()
    plt.show()


def experiment_three():
    n = 20
    p = 0.5
    w = 5
    original_list = []
    r1_list = []
    # create 100 graphs
    for i in range(0, 20):
        er = create_connected_graph(n, p, w)
        original_list.append(er.number_of_edges())  # add number of edges
        sorted_edges = sort_edges(er)
        new_h1 = build_h(er, sorted_edges, 1)
        r1_list.append(new_h1.number_of_edges())  # add number of edges

    N = 20
    ind = np.arange(N)  # the x locations for the groups
    p1 = plt.bar(ind, tuple(original_list), color='b', width = 0.5, facecolor='#9999ff', edgecolor='white')
    p2 = plt.bar(ind +0.5, tuple(r1_list), color='r', width = 0.5, facecolor='#ff9999', edgecolor='white')
    # plt.set_xticks(bar_width)

    plt.ylabel('Number of edges')
    plt.title('experiment 3')
    plt.legend((p1[0], p2[0]), ('original graph', 'spanner graph'))
    plt.show()


def experiment_four():
    n = 100
    w = 50
    tmp_original_edges_list = []
    tmp_spanner_edges_list = []
    for j in range(1, 11, 1):
        p = j/10.0
        tmp_original_edges = 0
        tmp_spanner_edges = 0
        for i in range(0, 20):
            er = create_connected_graph(n, p, w)
            tmp_original_edges = tmp_original_edges + er.number_of_edges()  # add number of edges
            sorted_edges = sort_edges(er)
            new_h3 = build_h(er, sorted_edges, 4)
            tmp_spanner_edges = tmp_spanner_edges + new_h3.number_of_edges()    # add number of edges
        tmp_original_edges_list.append(tmp_original_edges / 20)
        tmp_spanner_edges_list.append(tmp_spanner_edges / 20)

    plt.subplot(2,1,1)
    plt.title('experiment 4')
    plt.plot([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1], tmp_spanner_edges_list, marker='o')
    plt.xlabel('density of the graph')
    plt.ylabel('spanner graph - number of edges')
    plt.ylim(100, 150)
    plt.subplot(2,1,2)
    plt.plot([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1], tmp_original_edges_list, marker='o')
    plt.xlabel('density of the graph')
    plt.ylabel('original graph - number of edges')
    plt.legend()
    plt.show()


def experiment_five(r):
    n = 100
    p = 0.5
    tmp_original_edges_list = []
    tmp_spanner_edges_list = []
    for w in range(5, 105, 5):
        tmp_original_edges = 0
        tmp_spanner_edges = 0
        for i in range(0, 20):
            er = create_connected_graph(n, p, w)
            tmp_original_edges = tmp_original_edges + er.number_of_edges()  # add number of edges
            sorted_edges = sort_edges(er)
            new_h3 = build_h(er, sorted_edges, r)
            tmp_spanner_edges = tmp_spanner_edges + new_h3.number_of_edges()    # add number of edges
        tmp_original_edges_list.append(tmp_original_edges / 20)
        tmp_spanner_edges_list.append(tmp_spanner_edges / 20)

    plt.title('experiment 5')
    plt.plot(list(np.arange(5,105,5)), tmp_spanner_edges_list, marker='o')
    plt.xticks(list(np.arange(5,105,5)))
    plt.xlabel("weight range")
    plt.ylabel('spanner graph - number of edges')
    plt.legend()
    plt.show()


def main():
    option_num = input('Please choose number of experiment to conduct. choose 0 if you want to conduct an experiment with your own parameters\n'
                       '0 - Conduct yours experiment\n'
                       '1 - Experiment 1\n'
                       '2 - Experiment 2\n'
                       '3 - Experiment 3\n'
                       '4 - Experiment 4\n'
                       '5 - Experiment 5\n')
    if option_num == 0:
        conduct_yours_experiment()
    elif option_num == 1:
        experiment_one()
    elif option_num == 2:
        experiment_two()
    elif option_num == 3:
        experiment_three()
    elif option_num == 4:
        experiment_four()
    elif option_num == 5:
        exper5_r = input("enter stretch factor")
        experiment_five(exper5_r)


if __name__== "__main__":
    main()
