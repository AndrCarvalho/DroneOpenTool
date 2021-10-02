# -*- coding: utf-8 -*-
import Data_Collector as DC
import GeodesicGrids as GT
import Planner as PL
import RestrictionChecker as RC
import OutputFormatter as OF

import networkx.readwrite as R_W

from math import cos, asin, sqrt

import pyproj
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

cors = CORS(app, resource={
    r"/*":{
        "origins": "*"
    }
})
@app.route("/")
def home():
    return render_template('flask-DroneOpenTool.html')

@app.route('/pre_compute', methods=['POST'])
@cross_origin()
def pre_compute():
    area = request.form['area']
    start = request.form['s_loc']
    end = request.form['e_loc']

    start = (float(start[1:-1].split(',')[0]), float(start[1:-1].split(',')[1]))
    end = (float(end[1:-1].split(',')[0]), float(end[1:-1].split(',')[1]))

    center_pos_lock =[(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]

    geodesic = pyproj.Geod(ellps='WGS84')  # notice: [lon lat] notation!!!
    fwd_azimuth, back_azimuth, distance_s_e = geodesic.inv(start[1], start[0], end[1],end[0])


    if distance_s_e <= 500:
        zoom = 17
    elif distance_s_e <= 1200:
        zoom = 16
    elif distance_s_e <= 2600:
        zoom = 15
    elif distance_s_e <= 6000:
        zoom = 14
    else:
        zoom = 13

    return jsonify({'center_lock_lat': str(center_pos_lock[0]),'center_lock_lng': str(center_pos_lock[1]),'zoom':zoom,'distance': str(round(distance_s_e,1))})

@app.route('/compute', methods=['POST'])
@cross_origin()
def compute():
    print("compute: Recieved Request")
    area = request.form['area']
    restric = request.form['restric']
    start = request.form['s_loc']
    end = request.form['e_loc']
    g_granu = request.form['g_granu']
    g_margin = request.form['g_margin']

    restrictions = {}
    restricted_points = {}

    start = (float(start[1:-1].split(',')[0]), float(start[1:-1].split(',')[1]))
    end = (float(end[1:-1].split(',')[0]), float(end[1:-1].split(',')[1]))
    missionGrid = GT.createRectangularGrid(start, end, int(g_granu))

    e = 0.0001  # latch inclusion
    lats, lons = [tup[0] for tup in missionGrid['bounds']], [tup[1] for tup in missionGrid['bounds']]
    area = (min(lats) - e, min(lons) - e, max(lats) + e, max(lons) + e)
    missionGrid['outline'] = area

    for res in restric.split(','):
        if res == 'buildings':
            restrictions["buildings_nodes"], restrictions["buildings_ways"] = DC.collect_OSM_data(res, area)
            restricted_points["buildings"] = RC.inv_node_filter(missionGrid, restrictions["buildings_ways"])
        if res == 'water':
            restrictions["watArea_nodes"], restrictions["watArea_ways"] = DC.collect_OSM_data(res, area)
            restricted_points["watAreas"] = RC.inv_node_filter(missionGrid, restrictions["watArea_ways"])
        if res == 'residential':
            restrictions["resAreas_nodes"], restrictions["resAreas_ways"] = DC.collect_OSM_data(res, area)
            restricted_points["resAreas"] = RC.inv_node_filter(missionGrid, restrictions["resAreas_ways"])
        if res == 'woods':
            restrictions["woodsAreas_nodes"], restrictions["woodsAreas_ways"] = DC.collect_OSM_data(res, area)
            restricted_points["woodsAreas"] = RC.inv_node_filter(missionGrid, restrictions["woodsAreas_ways"])
        if res == 'military':
            restrictions["militaryAreas_nodes"], restrictions["militaryAreas_ways"] = DC.collect_OSM_data(res, area)
            restricted_points["militaryAreas"] = RC.inv_node_filter(missionGrid, restrictions["militaryAreas_ways"])
        if res == 'aero':
            restrictions["airport_nodes"], restrictions["airport_ways"] = DC.collect_OSM_data(res, area)
            restricted_points["airportAreas"] = RC.inv_node_filter(missionGrid, restrictions["airport_ways"])

    Graph = PL.construct_grid_graph(missionGrid, restricted_points, int(g_margin))

    Path = PL.a_star_path_cost(missionGrid, Graph)

    return jsonify(OF.path_to_JsonInterface(missionGrid,Path))


@app.route('/compute_rest', methods=['POST'])
@cross_origin()
def compute_rest():
    print("compute_rest: Recieved Request")
    start = request.form['s_loc']
    end = request.form['e_loc']


    Graph = R_W.read_gpickle("saves\Graph_restrictedAreaTagus.grx")

    start = (float(start[1:-1].split(',')[0]), float(start[1:-1].split(',')[1]))
    end = (float(end[1:-1].split(',')[0]), float(end[1:-1].split(',')[1]))

    graph_start = closest(Graph.nodes, start)
    graph_end = closest(Graph.nodes, end)

    e = 0.0001  # latch inclusion
    lats, lons = [tup[0] for tup in [[-9.3160717558923, 38.7440769943071], [-9.2802097558923, 38.7440769943071], [-9.2802062444515, 38.7300329972347], [-9.3160682444515, 38.7300329972347], [-9.3160717558923, 38.7440769943071]]],\
                 [tup[1] for tup in [[-9.3160717558923, 38.7440769943071], [-9.2802097558923, 38.7440769943071], [-9.2802062444515, 38.7300329972347], [-9.3160682444515, 38.7300329972347], [-9.3160717558923, 38.7440769943071]]]
    area = (min(lats) - e, min(lons) - e, max(lats) + e, max(lons) + e)

    #star + end and the rest of the properties from the offline computed graph
    missionGrid = {"start": graph_start, "end": graph_end,  # vv the rest below vv
                   "n_points": 700, "distance_s_e": distance(graph_start[0],graph_start[1],graph_end[0],graph_end[1]),
                   "neighbour": 4, "fur_neighbour": 6, "bounds": [[-9.3160717558923, 38.7440769943071], [-9.2802097558923, 38.7440769943071], [-9.2802062444515, 38.7300329972347], [-9.3160682444515, 38.7300329972347], [-9.3160717558923, 38.7440769943071]],
                   "margin_lvl": 3, "outline": area}  # not certain

    Path = PL.a_star_path_cost(missionGrid, Graph)
    # print(Path)
    return jsonify(OF.path_to_JsonInterface(missionGrid, Path))


##Auxiliar functions
#Thank you stackoverflow
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

def closest(data, point):
    return min(data, key=lambda p: distance(point[0],point[1],p[0],p[1]))


if __name__ == "__main__":
    app.run(debug=True)