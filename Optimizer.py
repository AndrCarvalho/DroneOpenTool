import pyproj

geodesic = pyproj.Geod(ellps='WGS84') #notice: [lon lat] notation!!!

# Removes co-linear points in sequence, do multiple times to remove every occurrence.
def remove_path_excess(path):
    new_path = []
    new_path.append(path[0])
    for i in range(0, len(path)-1, 2):

        if i + 2 >= len(path):
            continue


        #Project
        fw_az1, bck_az1, dist1 = geodesic.inv(path[i][1], path[i][0], path[i + 1][1], path[i + 1][0])
        fw_az2, bck_az2, dist2 = geodesic.inv(path[i + 1][1], path[i + 1][0], path[i + 2][1], path[i + 2][0])

        '''
        fw_az1, bck_az1, dist1 = geodesic.inv(path[i][0], path[i][1],
                                              path[i + 1][0], path[i + 1][1])  ## modified test version = (...[0], ...[1])
        fw_az2, bck_az2, dist2 = geodesic.inv(path[i + 1][0], path[i + 1][1],
                                              path[i + 2][0], path[i + 2][1])  ## modified test version = (...[0], ...[1])
        '''

        if abs(fw_az2 - fw_az1) >= 5:
            new_path.append(path[i + 1])
        new_path.append(path[i + 2])

    if path[len(path)-1] not in new_path:
        new_path.append(path[len(path)-1])

    #print("smooth:", new_path)
    return new_path


def smooth_path(path):
    new_path = []
    new_path.append(path[0])
    for i in range(0, len(path)-1, 2):

        if i + 2 >= len(path):
            continue

        #Project
        fw_az1, bck_az1, dist1 = geodesic.inv(path[i][1], path[i][0], path[i + 1][1], path[i + 1][0])
        fw_az2, bck_az2, dist2 = geodesic.inv(path[i + 1][1], path[i + 1][0], path[i + 2][1], path[i + 2][0])
        '''

        fw_az1, bck_az1, dist1 = geodesic.inv(path[i][0], path[i][1],
                                              path[i + 1][0], path[i + 1][1])  ## modified test version = (...[0], ...[1])
        fw_az2, bck_az2, dist2 = geodesic.inv(path[i + 1][0], path[i + 1][1],
                                              path[i + 2][0], path[i + 2][1])  ## modified test version = (...[0], ...[1])
        '''

        if abs(abs(fw_az2 - fw_az1) - 45) <= 5:
            pass  # remove
        else:
            #print("iter:", i, "--------------")
            #print("fw_az1:", fw_az1)
            #print("fw_az2:", fw_az2)
            #print("iter:", i, "--------------")
            #print(path[i + 1])
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
    print("Initial path:", len(initial_path), " | Remove Excess path:", len(path))
    print("Difference path excess:", len(initial_path) - len(path))

    n_excess_path = path
    path = smooth_path(path)
    print("Non-excess path:", len(n_excess_path), " | Smooth path:", len(path))
    print("Difference path smoothing:", len(n_excess_path) - len(path))
    return path
'''
##Testing
path_1 = [[-9.30413, 38.73852], [-9.303863, 38.738234], [-9.303597, 38.737949], [-9.303658, 38.737475], [-9.303391, 38.73719], [-9.303125, 38.736904], [-9.302858, 38.736619], [-9.302591, 38.736333], [-9.301997, 38.736236], [-9.30173, 38.73595]]

path_exc = remove_path_excess(path_1)
print(path_exc)

path_opt = optimize_path(path_1)
#path_opt = smooth_path(path_opt)
print("1:",path_1)
print("len(1):",len(path_1))
print("2:",path_opt)
print("len(2):",len(path_opt))
'''