# -*- coding: utf-8 -*-
from datetime import datetime
import Data_Collector as DC
import GeodesicGrids as GT
import Planner as PL
import RestrictionChecker as RC
import OutputFormatter as OF
import networkx.readwrite as R_W


# Input:
#   -> name = string :: name in which to address the plan
#   -> start = (lat, lon) tuple
#   -> goal = (lat, lon) tuple
#   -> granularity = integer[2 - ∞ ] :: Don't try over-exaggerated number:: (recommended 12 to 1500)
#   -> marginlvl = integer[0 - ∞ ] :: Don't try over-exaggerated number::  (recommended 0 to 5)
#   -> restrictions = list('restriction name', ... ) :: Possible values ['buildings',  'airways', 'residential', 'water', 'woods', 'military'] ::

def online_runner(name, start, goal, granularity, marginlvl, restrictions, obstacle_weight=10000):
    start_start = datetime.now()
    print(start_start)

    ### Create the problem structure

    missionGrid = GT.createRectangularGrid(start, goal, granularity)
    end_Grid = datetime.now()

    ### Fetch restrictions
    # (south,west,north,east)
    e = 0.0001  # latch inclusion
    lats, lons = [tup[0] for tup in missionGrid['bounds']], [tup[1] for tup in missionGrid['bounds']]
    area = (min(lats) - e, min(lons) - e, max(lats) + e, max(lons) + e)

    restriction_dict = {}
    for restr in restrictions:
        try:
            nodes, ways = DC.collect_OSM_data(restr, area)
            restr_name = restr + '_ways'
            restriction_dict[restr_name] = ways
        except:
            print("Not included restr " + restr)

    end_OSM = datetime.now()

    end_res = datetime.now()
    print("Problem Structure: Collected")

    ### Generate a graph from the problem structure
    Graph = PL.construct_grid_graph(missionGrid, {}, marginlvl)  # dynamic

    # R_W.write_gpickle(Graph,"saves\Online\"+name+".grx") # needed in online ? parameter?
    end_contructG = datetime.now()

    ### Search/Plan path

    Path = PL.a_star_path_cost(missionGrid, Graph)

    ### Check if the path violates any restrictions [in dynamic: updates costs of restricted nodes whenever it finds them]-- rename funtion to "repath"
    check = False
    num_decarted_nodes = []
    while (not check):

        check_b, unwanted_no_b = RC.path_check_good(Path, restriction_dict['buildings_ways'])
        # check_res, unwanted_no_res = RC.path_check_good(Path, resAreas_ways) #mod

        check = check_b
        num_decarted_nodes = set(num_decarted_nodes).union(unwanted_no_b)  # .union(unwanted_no_res)

        for i in unwanted_no_b:
            # Graph.remove_node(i)
            Graph = PL.update_weights(Graph, i, marginlvl, obstacle_weight)

        if not check:
            Path = PL.a_star_path_cost(missionGrid, Graph)

    # print('\n'.join(str(line)[1:-1] for line in num_decarted_nodes))

    end_planningPath = datetime.now()

    print("--Final Path--", str(end_planningPath - end_contructG))
    print("-num descarted nodes:", len(num_decarted_nodes))
    end_end = datetime.now()

    print("Collecting OSM data:", str(end_Grid - start_start))
    print("Creating Grid:", str(end_OSM - end_Grid))
    print("Restrited points:", str(end_res - end_OSM))
    print("Constructing Graph:", str(end_contructG - end_res))
    print("Path Planning:", str(end_planningPath - end_contructG))
    print("Total time:", str(end_end - start_start))

    OF.path_to_html(name, area, missionGrid, Path, marginlvl, "di")

    print("Done")


online_runner("Testing_Online_Runner", (38.7166, -9.4603), (38.7094, -9.4607), 200, 3, ['buildings', 'woods'])
