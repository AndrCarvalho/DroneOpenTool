from datetime import datetime
import Data_Collector as DC
import GeodesicGrids as GT
import Planner as PL
import RestrictionChecker as RC
import OutputFormatter as OF
#import geojson

start_start = datetime.now()
print(start_start)
###1- Fetch restrictions | such as buildings, residential areas or natural water formations

area= ( 40.6261, -8.6522, 40.6434, -8.6377) #Aveiro


buildings_nodes, buildings_ways = DC.collectBuildings_OSM_data(area)
#resAreas_nodes, resAreas_ways = DC.collectResAreas_OSM_data(area)
watArea_nodes, watArea_ways = DC.collectWaterAreas_OSM_data(area)

restrictions = {
    "buildings_nodes": buildings_nodes,
    "buildings_ways": buildings_ways,
#    "resAreas_nodes": resAreas_nodes,
#    "resAreas_ways": resAreas_ways
    "watArea_nodes": watArea_nodes,
    "watArea_ways": watArea_ways
}

end_OSM = datetime.now()

###2- Create the problem structure

missionGrid = GT.createRectangularGrid((40.64025, -8.64477), (40.63186, -8.64655),300)#Location5(Aveiro)

end_Grid = datetime.now()

#used in static r_cost

restricted_points = {
    "buildings": RC.inv_node_filter(missionGrid, buildings_ways),
    #"resAreas": RC.inv_node_filter(missionGrid, resAreas_ways),
    "watAreas": RC.inv_node_filter(missionGrid, watArea_ways)
}


end_res = datetime.now()
print("Problem Structure: Collected")

###3- Generate a graph from the problem structure
margin_lvl = 5
Graph = PL.construct_grid_graph(missionGrid, restricted_points, margin_lvl) #static
#Graph = PL.construct_grid_graph(missionGrid, [], margin) #dinamic

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

print('\n'.join(str(line)[1:-1] for line in num_decarted_nodes))

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

OF.path_to_html("Aveiro",area,missionGrid,Path,margin_lvl,"stat")

print("Done")