# -*- coding: utf-8 -*-
import overpy
#Input:
# squared_area= (south,west,north,east) .. example (40.63812063836527,-7.933373451232911,40.66009893471535,-7.8971529006958)

#TODO: dictionary with all the key-words per restriction like: {"building": '"building"', "residential": '"landuse"="residential"' ... }
# and aplly it to only 1 function
def collectBuildings_OSM_data(squared_area):
    api = overpy.Overpass()

    bbox = str(squared_area)

    query = """
    [out:json][timeout:25];
    (
    way["building"]"""+ bbox +""";
    >;
    relation["building"]"""+ bbox +""";
    >>;
    );
    out body;
    """
    try:
        result = api.query(query)
    except:
        print("Query failed..")
        return
    

    building_ways = []
    building_nodes = []

    for way in result.ways:
        building_ways.append(way)
        for num, node in enumerate(way.nodes):
            building_nodes.append(node)

    building_ways = list(dict.fromkeys(building_ways))  # buildings
    building_nodes = list(dict.fromkeys(building_nodes)) # nodes of ways

    print("Number of Buildings:",len(building_ways))
    return building_nodes, building_ways


def collectAero_OSM_data(squared_area):
    api = overpy.Overpass()

    bbox = str(squared_area)

    query = """
    [out:json][timeout:25];
    (
    way["aeroway"="aerodrome"]""" + bbox + """;
    >;
    relation["aeroway"="aerodrome"]""" + bbox + """;
    >>;
    );
    out body;
    """
    try:
        result = api.query(query)
    except:
        print("Query failed..")
        return

    aero_ways = []
    aero_nodes = []

    for way in result.ways:
        aero_ways.append(way)
        for num, node in enumerate(way.nodes):
            aero_nodes.append(node)

    for r in result.relations:
        for r_way in aux_get_element(r.id, result.relations).members:
           aero_ways.append(aux_get_element(r_way.ref, result.ways))

    aero_ways = list(dict.fromkeys(aero_ways))  # aero
    aero_nodes = list(dict.fromkeys(aero_nodes))  # nodes of ways

    print("Number of Aerospots:", len(aero_ways))
    return aero_nodes, aero_ways

def collectResAreas_OSM_data(squared_area):
    api = overpy.Overpass()

    bbox = str(squared_area)

    query = """
    [out:json][timeout:25];
    (
    way["landuse"="residential"]"""+ bbox +""";
    >;
    relation["landuse"="residential"]"""+ bbox +""";
    >>;
    );
    out body;
    """
    try:
        result = api.query(query)
    except:
        print("Query failed..")
        return


    resArea_ways = []
    resArea_nodes = []

    for way in result.ways:
        resArea_ways.append(way)
        for num, node in enumerate(way.nodes):
            resArea_nodes.append(node)

    resArea_ways = list(dict.fromkeys(resArea_ways))  # residential areas
    resArea_nodes = list(dict.fromkeys(resArea_nodes)) # nodes of ways

    print("Number of Residential Areas:", len(resArea_ways))
    return resArea_nodes, resArea_ways

def collectWaterAreas_OSM_data(squared_area):
    api = overpy.Overpass()

    bbox = str(squared_area)

    query = """
    [out:json][timeout:25];
    (
    way["natural"="water"]"""+ bbox +""";
    >;
    relation["natural"="water"]"""+ bbox +""";
    >>;
    );
    out body;
    """
    try:
        result = api.query(query)
    except:
        print("Query failed..")
        return

    watArea_ways = []
    watArea_nodes = []

    for way in result.ways:
        watArea_ways.append(way)
        for num, node in enumerate(way.nodes):
            watArea_nodes.append(node)
    '''
    for r in result.relations:
        for r_way in aux_get_element(r.id, result.relations).members:
           watArea_ways.append(aux_get_element(r_way.ref, result.ways))
    '''
    watArea_ways = list(dict.fromkeys(watArea_ways))  # water lakes/spots
    watArea_nodes = list(dict.fromkeys(watArea_nodes)) # nodes of ways

    print("Number of Water Areas:", len(watArea_ways))
    return watArea_nodes, watArea_ways

def collectWoodsAreas_OSM_data(squared_area):
    api = overpy.Overpass()

    bbox = str(squared_area)

    query = """
    [out:json][timeout:25];
    (
    way["natural"="wood"]"""+ bbox +""";
    >;
    relation["natural"="wood"]"""+ bbox +""";
    >>;
    );
    out body;
    """
    try:
        result = api.query(query)
    except:
        print("Query failed..")
        return

    woodArea_ways = []
    woodArea_nodes = []

    for way in result.ways:
        woodArea_ways.append(way)
        for num, node in enumerate(way.nodes):
            woodArea_nodes.append(node)

    for r in result.relations:
        for r_way in aux_get_element(r.id, result.relations).members:
           woodArea_ways.append(aux_get_element(r_way.ref, result.ways))

    woodArea_ways = list(dict.fromkeys(woodArea_ways))  # woods / forests
    woodArea_nodes = list(dict.fromkeys(woodArea_nodes)) # nodes of ways

    print("Number of Woods Areas:", len(woodArea_ways))
    return woodArea_nodes, woodArea_ways

#landuse	military

def collectMilitaryAreas_OSM_data(squared_area):
    api = overpy.Overpass()

    bbox = str(squared_area)

    query = """
    [out:json][timeout:25];
    (
    way["landuse"="military"]"""+ bbox +""";
    >;
    relation["landuse"="military"]"""+ bbox +""";
    >>;
    );
    out body;
    """
    try:
        result = api.query(query)
    except:
        print("Query failed..")
        return

    militaryArea_ways = []
    militaryArea_nodes = []

    for way in result.ways:
        militaryArea_ways.append(way)
        for num, node in enumerate(way.nodes):
            militaryArea_nodes.append(node)

    for r in result.relations:
        for r_way in aux_get_element(r.id, result.relations).members:
           militaryArea_ways.append(aux_get_element(r_way.ref, result.ways))

    militaryArea_ways = list(dict.fromkeys(militaryArea_ways))  # woods / forests
    militaryArea_nodes = list(dict.fromkeys(militaryArea_nodes)) # nodes of ways

    print("Number of Military Areas:", len(militaryArea_ways))
    return militaryArea_nodes, militaryArea_ways

def aux_get_element(id,list):
    for i in list:
        if id == i.id:
            return i

def print_all_nodesCollected(list_nodes):
    for num, node in enumerate(list_nodes):
        print(str(num) + " -> lat=", node.lat, " | lon=", node.lon)
