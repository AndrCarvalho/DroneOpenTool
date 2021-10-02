# -*- coding: utf-8 -*-
import pyproj
import numpy as np

geodesic = pyproj.Geod(ellps='WGS84')  # notice: [lon lat] notation!!!


# DONE: Creates a Square grid of points from the start point to goal point,
# being such that start and goal are on the middle of the opposite smaller edges of the rectangle;
# INPUT: start point, end point, number of points in the line connecting start to goal points
# RETURNS: dictionary that include a list of points that for the "grid" (lat | lon)
def createSquareGrid(start, end, n_points):  ##outdated see rectangular
    listNodes = {}
    listNodes["n_points"] = n_points
    listNodes["start"], listNodes["end"] = start, end
    listNodes["grid"] = []

    fwd_azimuth, back_azimuth, distance_s_e = geodesic.inv(start[1], start[0], end[1], end[0])
    print("distance start to end:", distance_s_e, "m")  # straigth line

    n = n_points  # n_points in a line
    distance = distance_s_e / n
    print("distance between nodes:", round(distance), "m")
    listNodes["neighbour"] = distance
    furthest_neighbour = (distance ** 2 + distance ** 2) ** 0.5
    print("furthest neighbour:", round(furthest_neighbour), "m")
    listNodes["fur_neighbour"] = furthest_neighbour

    for x in range(round(n / 2), -round(n / 2) - 1, -1):
        A_lon, A_lat, A_b_az = geodesic.fwd(start[1], start[0], fwd_azimuth - 90, x * distance)
        B_lon, B_lat, B_b_az = geodesic.fwd(end[1], end[0], fwd_azimuth - 90, x * distance)

        listNodes["grid"].append((A_lat, A_lon))

        result = geodesic.npts(A_lon, A_lat, B_lon, B_lat, n)
        for lon, lat in result:
            listNodes["grid"].append((lat, lon))

        listNodes["grid"].append((B_lat, B_lon))

    print("Starting point:", listNodes["start"])
    print("Ending point:", listNodes["end"])
    print("Number of grid nodes:", len(listNodes["grid"]))

    print(listNodes)
    return listNodes

# SquareGrid function not up-to-date

def createRectangularGrid(start, end, n_points):
    listNodes = {"n_points": n_points, "start": start, "end": end}
    print("Starting point:", listNodes["start"])
    print("Ending point:", listNodes["end"])

    listNodes["grid"] = []
    listNodes["npgrid_lat"] = np.zeros((round(n_points / 2) + 1, n_points))
    listNodes["npgrid_lon"] = np.zeros((round(n_points / 2) + 1, n_points))

    fwd_azimuth, back_azimuth, distance_s_e = geodesic.inv(start[1], start[0], end[1], end[0])
    listNodes["distance_s_e"] = distance_s_e
    print("Distance from start to end:", round(distance_s_e, 2), "m")  # straight line

    n = n_points - 2  # number of points in a line excluding start and end
    distance = distance_s_e / n_points
    print("Distance between points:", round(distance), "m")
    listNodes["neighbour"] = distance
    furthest_neighbour = (distance ** 2 + distance ** 2) ** 0.5
    print("Furthest neighbour point:", round(furthest_neighbour), "m")
    listNodes["fur_neighbour"] = furthest_neighbour

    listNodes['bounds'] = []

    i = 0
    j = 0

    if round(n_points / 4) % 2 != 0:
        temp = round(n_points / 4)
    else:
        temp = round(n_points / 4) - 1
    for x in range(temp, -temp - 1, -1):
        j = 0
        A_lon, A_lat, A_b_az = geodesic.fwd(start[1], start[0], fwd_azimuth - 90, x * distance)
        B_lon, B_lat, B_b_az = geodesic.fwd(end[1], end[0], fwd_azimuth - 90, x * distance)

        if x == temp or x == -temp:
            listNodes['bounds'].append((round(A_lat, 13), round(A_lon, 13)))
            listNodes['bounds'].append((round(B_lat, 13), round(B_lon, 13)))

        listNodes["grid"].append((round(A_lat, 13), round(A_lon, 13)))
        listNodes["npgrid_lat"][i][j] = round(A_lat, 13)
        listNodes["npgrid_lon"][i][j] = round(A_lon, 13)
        j = j + 1

        result = geodesic.npts(A_lon, A_lat, B_lon, B_lat, n)
        for lon, lat in result:
            listNodes["grid"].append((round(lat, 13), round(lon, 13)))
            listNodes["npgrid_lat"][i][j] = round(lat, 13)
            listNodes["npgrid_lon"][i][j] = round(lon, 13)
            j = j + 1

        listNodes["grid"].append((round(B_lat, 13), round(B_lon, 13)))
        listNodes["npgrid_lat"][i][j] = round(B_lat, 13)
        listNodes["npgrid_lon"][i][j] = round(B_lon, 13)
        j = j + 1
        i = i + 1

    print("Number of grid points:", len(listNodes["grid"]))

    return listNodes
