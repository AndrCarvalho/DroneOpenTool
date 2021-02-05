# -*- coding: utf-8 -*-
from datetime import datetime
import Data_Collector as DC
import GeodesicGrids as GT
import Planner as PL
import RestrictionChecker as RC
import OutputFormatter as OF

import networkx.readwrite as R_W

start_start = datetime.now()
print(start_start)
###1- Fetch restrictions | such as buildings, residential areas or natural water formations

#(south,west,north,east)
#area= ( 38.73, -9.3044, 38.739, -9.2895) #Tagus_Location1
#area= ( 38.7333, -9.3044, 38.739, -9.2793) #Tagus_Location2
#rea= ( 38.7323, -9.3044, 38.739, -9.2697) #Tagus_Location3
#area= ( 38.7226, -9.3044, 38.739, -9.2588) #Tagus_Location4
#area= ( 38.7218, -9.3044, 38.739, -9.2473) #Tagus_Location5
#area= ( 38.7186, -9.3044, 38.739, -9.2367) #Tagus_Location6
#area= ( 38.7294, -9.3044, 38.739, -9.2226) #Tagus_Location7

area= (38.7300611, -9.3160718, 38.74404891, -9.2802098) # restricted area



buildings_nodes, buildings_ways = DC.collectBuildings_OSM_data(area)
#resAreas_nodes, resAreas_ways = DC.collectResAreas_OSM_data(area)
#watArea_nodes, watArea_ways = DC.collectWaterAreas_OSM_data(area)

restrictions = {
    "buildings_nodes": buildings_nodes,
    "buildings_ways": buildings_ways,
#    "resAreas_nodes": resAreas_nodes,
#    "resAreas_ways": resAreas_ways
#    "watArea_nodes": watArea_nodes,
#    "watArea_ways": watArea_ways
}

end_OSM = datetime.now()

###2- Create the problem structure

#missionGrid = GT.createRectangularGrid((38.7374, -9.3021), (38.7313, -9.2251),1100)#Tagus_Location7
#missionGrid = GT.createRectangularGrid((38.7374, -9.3021), (38.7196,-9.2383),970)#Tagus_Location6
#missionGrid = GT.createRectangularGrid((38.7374, -9.3021), (38.723, -9.2491),800)#Tagus_Location5
#missionGrid = GT.createRectangularGrid((38.7374, -9.3021), (38.7230,-9.2590),640)#Tagus_Location4
#missionGrid = GT.createRectangularGrid((38.7374, -9.3021), (38.7332, -9.2699),470)#Tagus_Location3
#missionGrid = GT.createRectangularGrid((38.7374, -9.3021), (38.7348, -9.281),300)#Tagus_Location2
#missionGrid = GT.createRectangularGrid((38.7374, -9.3021), (38.7369, -9.2908),160)#Tagus_Location1

missionGrid = GT.createRectangularGrid((38.737055, -9.31607), (38.737055,  -9.280208), 700) #figuring grid
#OF.print_grid_mapcos(missionGrid)

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
margin_lvl = 3
Graph = PL.construct_grid_graph(missionGrid, restricted_points, margin_lvl) #static
#Graph = PL.construct_grid_graph(missionGrid, [], margin_lvl) #dinamic

R_W.write_gpickle(Graph,"saves\Graph_restrictedAreaTagus.grx")
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
end_end = datetime.now()

print("Collecting OSM data:", str(end_OSM - start_start))
print("Creating Grid:", str(end_Grid - end_OSM))
print("Restrited points:", str(end_res - end_Grid))
print("Constructing Graph:",str(end_contructG - end_res))
print("Path Planning:",str(end_planningPath - end_contructG))
print("Total time:",str(end_end - start_start))

OF.path_to_html("Test_restrictedAreaTagus",area,missionGrid,Path,margin_lvl,"stat")

print("Done")