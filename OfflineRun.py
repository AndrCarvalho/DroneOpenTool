# -*- coding: utf-8 -*-
from datetime import datetime
import Data_Collector as DC
import GeodesicGrids as GT
import Planner as PL
import RestrictionChecker as RC
import Optimizer as OP
import OutputFormatter as OF
import networkx.readwrite as R_W


# Input:
#   -> name = string :: name in which to address the plan
#   -> start = (lat, lon) tuple
#   -> goal = (lat, lon) tuple
#   -> granularity = integer[2 - ∞ ] :: Don't try over-exaggerated number:: (recommended 12 to 1500)
#   -> marginlvl = integer[0 - ∞ ] :: Don't try over-exaggerated number::  (recommended 0 to 5)
#   -> restrictions = list('restriction name', ... ) :: Possible values ['buildings',  'airways', 'residential', 'water', 'woods', 'military'] ::
#   -> area = (south,west,north,east) (default None) :: 4-tuple of coordinates to define a rectangular area ::
#   -> obstacle_weight = integer [0 - ∞] (default 10000) :: importance of the obstacles ::

def offline_runner(name, start, goal, granularity, marginlvl, restrictions, area=None, obstacle_weight=10000):
    start_start = datetime.now()
    print(start_start)

    ### Create the problem structure

    missionGrid = GT.createRectangularGrid(start, goal, granularity)
    end_Grid = datetime.now()

    ### Fetch restrictions
    # (south,west,north,east)
    if area is None:
        e = 0.0001  # latch inclusion
        lats, lons = [tup[0] for tup in missionGrid['bounds']], [tup[1] for tup in missionGrid['bounds']]
        area = (min(lats) - e, min(lons) - e, max(lats) + e, max(lons) + e)

    restriction_dict = {}
    for restr in restrictions:
        try:
            nodes, ways = DC.collect_OSM_data(restr, area)
            restr_name = restr + '_ways'
            restriction_dict[restr_name] = ways
            #print(len(ways), ways)
        except:
            print("Not included restr " + restr)

    end_OSM = datetime.now()

    restricted_points = {}
    for restr in restriction_dict.keys():
        restricted_points[restr] = RC.inv_node_filter(missionGrid, restriction_dict[restr])

    end_res = datetime.now()
    print("Problem Structure: Collected")

    ### Generate a graph from the problem structure
    Graph = PL.construct_grid_graph(missionGrid, restricted_points, marginlvl, obstacle_weight)

    R_W.write_gpickle(Graph, name + "_gran"+ str(granularity)+"_mlvl"+str(marginlvl)+"--obs"+str(obstacle_weight)+".grx")
    end_contructG = datetime.now()

    ### Search/Plan path
    print("Planning...")
    Path = PL.a_star_path_cost(missionGrid, Graph)

    ### Check if the path violates any restrictions [in dynamic: updates costs of restricted nodes whenever it finds them]-- rename funtion to "repath"
    check = False
    num_decarted_nodes = []
    checks = {restr: False for restr in restriction_dict.keys()}
    while (not check):
        for restr in restriction_dict.keys():
            check_i, unwanted = RC.path_check_good(Path, restriction_dict[restr])
            num_decarted_nodes = set(num_decarted_nodes).union(unwanted)
            checks[restr] = check_i

            for i in unwanted:
                # Graph.remove_node(i)
                Graph = PL.update_weights(Graph, i, marginlvl, obstacle_weight)

        if all(checks.values()):
            check = True

        if not check:
            oldPath = Path
            Path = PL.a_star_path_cost(missionGrid, Graph)
            if Path == oldPath:
                #print("Same output ...")
                check = True
                name += '[X]'

    end_planningPath = datetime.now()

    Path = OP.optimize_path(Path)

    end_smoothingPath = datetime.now()

    #print("--Final Path--", str(end_planningPath - end_contructG))
    #print("-num discarded nodes:", len(num_decarted_nodes))
    end_end = datetime.now()

    print("Creating Grid:", str(end_Grid - start_start))
    print("Collecting OSM data:", str(end_OSM - end_Grid))
    print("Restricted points:", str(end_res - end_OSM))
    print("Constructing Graph:", str(end_contructG - end_res))
    print("Path Planning:", str(end_planningPath - end_contructG))
    print("Optimizing Path", str(end_smoothingPath - end_planningPath))
    print("Total time:", str(end_end - start_start))

    OF.path_to_html(name, area, missionGrid, Path, marginlvl, "stat")

    print("Done")