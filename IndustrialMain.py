# -*- coding: utf-8 -*-
from datetime import datetime
import Data_Collector as DC
import GeodesicGrids as GT
import Planner as PL
import RestrictionChecker as RC
import OutputFormatter as OF

start_start = datetime.now()
print(start_start)
###1- Fetch restrictions | such as buildings, residential areas or natural water formations

#(south,west,north,east)
area= (39.820469,-8.897982,39.853818,-8.846140) #figuring area

buildings_nodes, buildings_ways = DC.collectBuildings_OSM_data(area)

restrictions = {
    "buildings_nodes": buildings_nodes,
    "buildings_ways": buildings_ways,
}

end_OSM = datetime.now()

for gran in [100, 200, 300, 400, 500, 600, 700, 800]:
    star_loop = datetime.now()
    print("\n\n")
    print("--------------------------------------------------------------------")
    print("GRAN:",gran)
    ###2- Create the problem structure

    missionGrid = GT.createRectangularGrid((38.73852, -9.30413), (38.73595, -9.30173),gran) #figuring grid

    end_Grid = datetime.now()

    #used in static r_cost

    restricted_points = {
        "buildings": RC.inv_node_filter(missionGrid, buildings_ways),
        #"resAreas": RC.inv_node_filter(missionGrid, resAreas_ways),
        #"watAreas": RC.inv_node_filter(missionGrid, watArea_ways)
    }


    end_res = datetime.now()
    print("Problem Structure: Collected")

    ###3- Generate a graph from the problem structure
    margin_lvl = 0
    Graph = PL.construct_grid_graph(missionGrid, restricted_points, margin_lvl) #static
    #Graph = PL.construct_grid_graph(missionGrid, [], margin_lvl) #dinamic

    end_contructG = datetime.now()

    ###4- Search the best path

    Path = PL.a_star_path_cost(missionGrid, Graph)

    ###5- Check if the path violates any restrictions [in dynamic: updates costs of restricted nodes whenever it finds them]-- rename funtion to "repath"
    check = False
    num_decarted_nodes = []
    while(not check):

        check_b, unwanted_no_b = RC.path_check_good(Path,buildings_ways)
        #check_res, unwanted_no_res = RC.path_check_good(Path, resAreas_ways) #mod

        check = check_b
        num_decarted_nodes = set(num_decarted_nodes).union(unwanted_no_b)#.union(unwanted_no_res)

        for i in unwanted_no_b:
            #Graph.remove_node(i)
            # obstacle_weight = 10000
            Graph = PL.update_weights(Graph, i, margin_lvl, 10000)

        if not check:
            Path = PL.a_star_path_cost(missionGrid, Graph)

    #print('\n'.join(str(line)[1:-1] for line in num_decarted_nodes))

    end_planningPath = datetime.now()

    print("--Final Path--",str(end_planningPath - end_contructG))
    print("-num descarted nodes:", len(num_decarted_nodes))
    #print("descarted nodes:", num_decarted_nodes)
    #OF.print_path_mapcos(missionGrid, Path)
    end_Mission = datetime.now()

    print("Collecting OSM data:", str(end_OSM - start_start))
    print("Creating Grid:", str(end_Grid - end_OSM))
    print("Restrited points:", str(end_res - star_loop))
    print("Constructing Graph:",str(end_contructG - end_res))
    print("Path Planning:",str(end_planningPath - end_contructG))
    print("Total Mission time:",str((end_Mission - star_loop) + (end_Grid - end_OSM)))

    OF.path_to_html("Test",area,missionGrid,Path,margin_lvl,"stat")
end_end = datetime.now()
print("Total time:",str(end_end - start_start))
print("Done")