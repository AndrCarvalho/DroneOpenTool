import pyproj

geodesic = pyproj.Geod(ellps='WGS84') #notice: [lon lat] notation!!!

# Removes co-linear points in sequence, do multiple times to remove every occurrence.
def remove_path_excess(path):
    new_path = [path[0]]
    for i in range(0, len(path)-1, 2):

        if i + 2 >= len(path):
            continue

        #Project
        fw_az1, bck_az1, dist1 = geodesic.inv(path[i][1], path[i][0], path[i + 1][1], path[i + 1][0])
        fw_az2, bck_az2, dist2 = geodesic.inv(path[i + 1][1], path[i + 1][0], path[i + 2][1], path[i + 2][0])

        if abs(fw_az2 - fw_az1) >= 5:
            new_path.append(path[i + 1])
        new_path.append(path[i + 2])

    if path[len(path)-1] not in new_path:
        new_path.append(path[len(path)-1])

    #print("smooth:", new_path)
    return new_path


def smooth_path(path):
    new_path = [path[0]]
    for i in range(0, len(path)-1, 2):

        if i + 2 >= len(path):
            continue

        #Project
        fw_az1, bck_az1, dist1 = geodesic.inv(path[i][1], path[i][0], path[i + 1][1], path[i + 1][0])
        fw_az2, bck_az2, dist2 = geodesic.inv(path[i + 1][1], path[i + 1][0], path[i + 2][1], path[i + 2][0])

        if abs(abs(fw_az2 - fw_az1) - 45) <= 5:
            pass  # remove
        else:
            new_path.append(path[i + 1])  # keep the node
        new_path.append(path[i + 2])

    if path[len(path)-1] not in new_path:
        new_path.append(path[len(path)-1])

    #print("smooth:", new_path)
    return new_path

def optimize_path(path):
    initial_path = path
    check = False
    while not check:
        old_path = path
        path = remove_path_excess(path)

        if path == old_path:
            check = True
    #print("Initial path:", len(initial_path), " | Remove Excess path:", len(path))
    #print("Difference path excess:", len(initial_path) - len(path))

    n_excess_path = path
    path = smooth_path(path)
    #print("Non-excess path:", len(n_excess_path), " | Smooth path:", len(path))
    #print("Difference path smoothing:", len(n_excess_path) - len(path))
    print("Points removed:", str(len(initial_path) - len(path)))
    return path
