# -*- coding: utf-8 -*-
import overpy

RESTRICTIONS = {'buildings': """ "building" """,
                'airways': """ "aeroway"="aerodrome" """,
                'residential': """ "landuse"="residential" """,
                'water': """ "natural"="water" """,
                'woods': """ "natural"="wood" """,
                'military': """ "landuse"="military" """
                }


def collect_OSM_data(restr, area):
    api = overpy.Overpass()

    bbox = str(area)

    query = """
        [out:json][timeout:25];
        (
        way[""" + RESTRICTIONS[restr] + """]""" + bbox + """;
        >;
        relation[""" + RESTRICTIONS[restr] + """]""" + bbox + """;
        >>;
        );
        out body;
        """
    try:
        result = api.query(query)
    except:
        print("Query failed..")
        return

    ways = []
    nodes = []

    for way in result.ways:
        ways.append(way)
        for num, node in enumerate(way.nodes):
            nodes.append(node)

    for r in result.relations:
        for r_way in aux_get_element(r.id, result.relations).members:
            ways.append(aux_get_element(r_way.ref, result.ways))

    ways = list(dict.fromkeys(ways))
    nodes = list(dict.fromkeys(nodes))

    print("Number of " + restr + ":", len(ways))
    return nodes, ways


def aux_get_element(id, list):
    for i in list:
        if id == i.id:
            return i


def print_all_nodesCollected(list_nodes):
    for num, node in enumerate(list_nodes):
        print(str(num) + " -> lat=", node.lat, " | lon=", node.lon)
