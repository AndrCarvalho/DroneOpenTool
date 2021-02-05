# -*- coding: utf-8 -*-
def isInsideRestriction(lat, lon, way_nodes):
    #print("Coordenada:", lat, lon)

    nodes_minX, nodes_maxX = way_nodes[0].lat, way_nodes[0].lat
    nodes_minY, nodes_maxY = way_nodes[0].lon, way_nodes[0].lon

    for node in way_nodes:
        x, y = node.lat, node.lon

        nodes_minX, nodes_maxX = min(nodes_minX,x), max(nodes_maxX,x)
        nodes_minY, nodes_maxY = min(nodes_minY,y), max(nodes_maxY,y)

    if lat < nodes_minX or lat > nodes_maxX or lon < nodes_minY or lon > nodes_maxY: return False

    inside = False

    j = len(way_nodes) - 1
    for i in range(len(way_nodes)):
        if ((way_nodes[i].lon > lon) != (way_nodes[j].lon > lon) and
                lat < (float(way_nodes[j].lat) - float(way_nodes[i].lat)) * (lon - float(way_nodes[i].lon)) / (float(way_nodes[j].lon) - float(way_nodes[i].lon)) + float(way_nodes[i].lat)):
            inside = not inside
        j=i
    return inside

#DONE: Function to evaluate if a chosen point is inside of any of ALL queried restrictions - return True for in | False for outside
def isInsideGLOBAL(lat, lon, all_ways):
    for way in all_ways:
        if isInsideRestriction(lat, lon, way.nodes):
            #print("It's inside:", lat, ",", lon)
            return True
    return False

#DONE: Filter that removes non-good nodes from 'listNodes' from fuction GeodTesting.createSquareGrid
def node_filter(listNodes, ways):
    new_list = listNodes['grid']
    points_filtered = 0
    for node in listNodes['grid']:
        if isInsideGLOBAL(node[0],node[1], ways):
            new_list.remove(node)
            points_filtered = points_filtered + 1
    listNodes['grid'] = new_list
    print("points_filtered:", points_filtered)
    return listNodes

#return non-good nodes
def inv_node_filter(listNodes, ways):
    new_list = []
    points_filtered = 0
    for node in listNodes['grid']:
        if isInsideGLOBAL(node[0],node[1], ways):
            new_list.append(node)
            points_filtered = points_filtered + 1
    if listNodes['start'] in new_list:
        new_list.remove(listNodes['start'])
    if listNodes['end'] in new_list:
        new_list.remove(listNodes['end'])
    print("points_filtered:", points_filtered)
    return new_list

def path_check_good(path,ways):
    unwanted_nodes = []
    for node in path:
        if isInsideGLOBAL(node[0], node[1], ways):
            unwanted_nodes.append(node)
    if unwanted_nodes:
        print("nw:", len(unwanted_nodes))
        return False, unwanted_nodes
    print("w:",len(unwanted_nodes))
    return True, unwanted_nodes
