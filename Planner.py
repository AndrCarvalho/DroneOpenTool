import networkx as nx
import pyproj

geodesic = pyproj.Geod(ellps='WGS84') #notice: [lon lat] notation!!!

def construct_grid_graph(listNodes, restricted_dic, margin):
    n_points = listNodes["n_points"]
    graph = nx.grid_2d_graph(round(n_points/2)+1,n_points)

    for edge in graph.edges:
        graph.edges[edge]['weight'] = listNodes["neighbour"]
        graph.edges[edge]['r_cost'] = listNodes["neighbour"]

    graph.add_edges_from([((x, y), (x + 1, y + 1)) for x in range((round(n_points/2)+1)-1) for y in range(n_points-1)] +
                     [((x + 1, y), (x, y + 1)) for x in range((round(n_points/2)+1)-1) for y in range(n_points-1)], weight=listNodes["fur_neighbour"], r_cost=listNodes["fur_neighbour"])

    dict_label = {}
    for i, j in graph.nodes():
        dict_label[(i,j)] = (listNodes["npgrid_lat"][i][j],listNodes["npgrid_lon"][i][j])

    nx.relabel_nodes(graph,dict_label,False)

    print("Updating.. Margin:",margin,"-", str(margin*listNodes["neighbour"]))

    for i in restricted_dic['buildings']:
        update_weights(graph, i, margin, 10000)

    for i in restricted_dic['watAreas']:
        # Graph.remove_node(i)
        update_weights(graph, i, margin, 10000)

    print("Updating..Over")

    return graph

def energy_from_AtoB_MaxS(pointA,pointB):

    speed = 26.1111111
    fwd_azimuth, back_azimuth, distance = geodesic.inv(pointA[1], pointA[0], pointB[1], pointB[0])

    time_to_travel = distance / speed

    return time_to_travel * energy_consump_sec()


def shortest_path(listNodes, graph):
    try:
        path = nx.shortest_path(graph, source=listNodes['start'], target=listNodes['end'])
    except:
        print("No path between Start and Goal locations available. Consider increasing/decreasing number of nodes.")
    return path

def a_star_path_cost(listNodes, graph):
    try:
        path = nx.astar_path(graph, source=listNodes['start'], target=listNodes['end'], heuristic=energy_from_AtoB_MaxS, weight='r_cost')
    except:
        print("No path between Start and Goal locations available. Consider increasing/decreasing number of nodes.")
    return path

def a_star_path_cost_indiv(start,target, graph):
    try:
        path = nx.astar_path(graph, start, target, heuristic=energy_from_AtoB_MaxS, weight='r_cost')
    except:
        print("No path between Start and Goal locations available. Consider increasing/decreasing number of nodes.")
    return path

def update_weights(graph, node, grade, s_weight):
    if grade > 1:
        for nbr in graph[node]:
            graph[nbr][node]['r_cost'] = s_weight
            update_weights(graph, nbr, grade-1, s_weight/grade)
    else:
        for nbr in graph[node]:
            graph[nbr][node]['r_cost'] = s_weight
    return graph

def energy_consump_sec():
    W = 3.44#Kg - Weight of the drone (DJI Inspire2) -> Max takeoff weight: 4.25 Kg
    m = 0.8#kg - Weight of the payload (0.81 kg max payload )
    g = 9.8#N - Gravity

    T = (W + m)*g # Trust

    p = 1.2041#Kg/m^3 - Air density at 20ºc
    s = 0.113411495# m^2 - Circle area of propeller with 38 centimeter (DJI Inspire 2 1550T)

    n_pr = 4# Number of propellers (DJI Inspire2)

    Power_f = ((W + m) ** (3 / 2)) * ((g ** 3) / (2 * p * s * n_pr)) ** 0.5 #W - power from all 4 propellers
    return Power_f