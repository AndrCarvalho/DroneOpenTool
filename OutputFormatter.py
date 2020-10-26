import geojson

def path_to_html(name,area,missionGrid,path,margin_lvl,method):
    center_pos = [(area[0] + area[2]) / 2, (area[1] + area[3]) / 2]
    start_geojson = geojson.Point((missionGrid['start'][1], missionGrid['start'][0]))
    end_geojson = geojson.Point((missionGrid['end'][1], missionGrid['end'][0]))

    path_geojson = geojson.LineString([(p[1], p[0]) for p in path])
    f = open("Demo Results/"+str(name) + "_" + str(missionGrid['n_points']) + "_" + str(margin_lvl) + "_" +str(method) +".html", "w")
    f.write(
        """<html>
        <head>
    	    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
            integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
            crossorigin=""/>
    	    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
            integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
            crossorigin=""></script>
        </head>
        <body>

            <div id="mapid" style="width:800px;height:600px"></div>
            <script>

            var mymap = L.map('mapid')
            .setView(""" + str(center_pos) + """,15);

            L.tileLayer('https://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png', {
                maxZoom: 18,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(mymap);

            var geojson_path = """ + str(path_geojson) + """
            var geojson_start = """ + str(start_geojson) + """
            var geojson_end = """ + str(end_geojson) + """

            L.geoJSON(geojson_path).addTo(mymap);
            L.geoJSON(geojson_start).addTo(mymap);
            L.geoJSON(geojson_end).addTo(mymap);
            L.control.scale().addTo(mymap);

            </script>
        </body>
        </html>""")
    '''
    f.write("var geojson_path = " + str(path_geojson) +"\n"+
            "var geojson_start = " + str(start_geojson)+"\n"+
            "var geojson_end = " + str(end_geojson))
    '''
    f.close()

def path_to_geojson(name,missionGrid,path,margin_lvl,method):
    start_geojson = geojson.Point((missionGrid['start'][1], missionGrid['start'][0]))
    end_geojson = geojson.Point((missionGrid['end'][1], missionGrid['end'][0]))

    path_geojson = geojson.LineString([(p[1], p[0]) for p in path])
    f = open("Demo Results/"+str(name) + "_" + str(missionGrid['n_points']) + "_" + str(margin_lvl) + "_" +str(method) +".geojson", "w")
    f.write(str(path_geojson) +"\n"+
            str(start_geojson)+"\n"+
            str(end_geojson))

    f.close()

def print_path_mapcos(listNodes, path):
    print(str(listNodes['start'])[1:-1] + " <green>")
    for node in path[1:-1]:
         print(str(node)[1:-1] + " <orange>")
    print(str(listNodes['end'])[1:-1] + " <red>")