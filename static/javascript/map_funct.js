var mymap = L.map('mapid')
//.setView([38.736806, -9.29845],15);
.setView([59.332136, 18.070979],15);
//console.log(mymap)

L.tileLayer('https://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(mymap);
L.control.scale().addTo(mymap)

//var geojson_restZ = {"coordinates": [[-9.3160717488681, 38.7440489063467], [-9.2802097488681, 38.7440489063467], [-9.280206251473, 38.7300610852626], [-9.316068251473, 38.7300610852626], [-9.3160717488681, 38.7440489063467]], "type": "LineString"}

//L.geoJSON(geojson_restZ).addTo(mymap);
//L.control.scale().addTo(mymap);

var popup = L.popup();

var cur_id = ''
function setCurId(id) {
    cur_id = id;
}

function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("GPS coordinates: " + e.latlng.toString().substr(6))
        .openOn(mymap);
    if (cur_id != '') {
        document.getElementById(cur_id).value = e.latlng.toString().substr(6)
        cur_id = ''
    }
}

mymap.on('click', onMapClick);

function pre_compute(name) {
    var area = "("+mymap.getBounds().getSouth()+","+mymap.getBounds().getWest()+","+mymap.getBounds().getNorth()+","+mymap.getBounds().getEast()+")";
    var s_loc = document.forms[name]["s_loc"].value;
    var e_loc = document.forms[name]["e_loc"].value;

    var res_build = document.forms[name]["res_build"].checked;

    if (s_loc == '' || e_loc == '' || s_loc == 'click on map' || e_loc == 'click on map') {
        console.log(" --- Computed nothing!")
    }else{
        //console.log("Area:" + area.toString() + " | Starting position:" + s_loc.toString() + " | End Position: " + e_loc.toString() +
        //" | Restrict:" + res_build.toString() + " --- Computed everything!")
        post_pre_data(area,res_build,s_loc,e_loc)
    }
}
function post_pre_data(area,res_build,s_loc,e_loc) {
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/pre_compute",
        data: { area: area, restric: res_build, s_loc: s_loc, e_loc: e_loc},
        success: callbackFunc
    });
}

function compute(name1,name2) {
    var area = "("+mymap.getBounds().getSouth().toFixed(6)+","+mymap.getBounds().getWest().toFixed(6)+","+mymap.getBounds().getNorth().toFixed(6)+","+mymap.getBounds().getEast().toFixed(6)+")";
    var s_loc = document.forms[name1]["s_loc"].value;
    var e_loc = document.forms[name1]["e_loc"].value;

    var restric = ""
    var checkboxes = document.querySelectorAll('input[type=checkbox]:checked')
    for (var i = 0; i < checkboxes.length; i++) {
        restric += "," + checkboxes[i].value;
    }

    var g_granu = document.forms[name2]["gran_slider"].value*50;
    var g_margin = document.forms[name2]["margin_slider"].value;


    if (s_loc == '' || e_loc == '' || s_loc == 'click on map' || e_loc == 'click on map') {
        console.log(" --- Computed nothing!")
    }else{
        //console.log("Area:" + area.toString() +
        //" | Starting position:" + s_loc.toString() +
        //" | End Position: " + e_loc.toString() +
        //" | Restrict:" + restric.toString()+
        //" | Granularity:" + g_granu.toString() +
        //" | Margin level:" + g_margin.toString() + "--- Computed everything!")
        post_data(area,restric,s_loc,e_loc,g_granu,g_margin)
    }
}
// Limited version
function post_data_rest(area,restric,s_loc,e_loc, g_granu, g_margin) {
    var element = document.getElementById("computeL");
    element.classList.add("button--loading");
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/compute_rest",
        data: { s_loc: s_loc, e_loc: e_loc},
        success: callbackFunc2
    });
}

function post_data(area, restric, s_loc, e_loc, g_granu, g_margin) {
    var element = document.getElementById("computeL");
    element.classList.add("button--loading");
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/compute",
        data: { area: area, restric: restric, s_loc: s_loc, e_loc: e_loc, g_granu: g_granu, g_margin: g_margin},
        success: callbackFunc2
    });
}


var g_distance = 0

function callbackFunc(response) {
    //console.log(response);
    g_distance = response['distance'];
    var di = document.getElementById("distance");
    di.innerHTML = "Distance: " + response['distance'] +" meters";
    di.style.visibility = "visible";
    document.getElementById("sliders").style.visibility = "visible";
    document.getElementById("gran_slider").style.visibility = "visible";
    document.getElementById("gran_output").style.visibility = "visible";
    mymap.setView(new L.LatLng(parseFloat(response['center_lock_lat']),parseFloat(response['center_lock_lng'])),parseInt(response['zoom']));
}

var s;
var e;
var p;
var r;
var b;

function callbackFunc2(response) {
    //console.log(response);
    var geojson_start = response[0]
    var geojson_end = response[1]
    var geojson_path = response[2]
    var geojson_resarea = response[3]
    var geojson_bounds = response[4]

    if (s != null){
        mymap.removeLayer(s);
        s = L.geoJSON(geojson_start);
        s.addTo(mymap);
        mymap.removeLayer(e);
        e = L.geoJSON(geojson_end);
        e.addTo(mymap);
        mymap.removeLayer(p);
        p = L.geoJSON(geojson_path);
        p.addTo(mymap);
        mymap.removeLayer(r);
        r = L.geoJSON(geojson_resarea,{ color: 'red', opacity:0.2 }).addTo(mymap);
        r.addTo(mymap);
        mymap.removeLayer(b);
        b = L.geoJSON(geojson_bounds,{ dashArray: '5,5', color: 'black', opacity:0.6 }).addTo(mymap);
        b.addTo(mymap);
    }else{
        s = L.geoJSON(geojson_start);
        s.addTo(mymap);
        e = L.geoJSON(geojson_end);
        e.addTo(mymap);
        p = L.geoJSON(geojson_path);
        p.addTo(mymap);
        r = L.geoJSON(geojson_resarea,{ color: 'red', opacity:0.2 }).addTo(mymap);
        r.addTo(mymap);
        b = L.geoJSON(geojson_bounds,{ dashArray: '5,5', color: 'black', opacity:0.6 }).addTo(mymap);
        b.addTo(mymap);
    }
    var element = document.getElementById("computeL");
    element.classList.remove("button--loading");
    window.location.hash = "results";
    var results = response[5]

    document.getElementById("results").style.visibility = "visible"

    //document.getElementById("debug").innerHTML = JSON.stringify(results);

    document.getElementById("total_distance").innerHTML = 'Total Distance: ' + results['total_dist'].toFixed(2) + ' meters';
    //document.getElementById("total_distance2x").innerHTML = 'Total Distance: ' + (results['total_dist']*2).toFixed(2) + ' meters';


    var date = new Date(0);
    date.setSeconds(results['travel_time_10ms_min']); // specify value for SECONDS here
    var timeString = date.toISOString().substr(11, 8);

    document.getElementById("travel_time").innerHTML = 'Travel Time (at 10 m/s): ' + timeString + ' minutes';

    //var date2x = new Date(0);
    //date2x.setSeconds(results['travel_time_10ms_min']*2); // specify value for SECONDS here
    //var timeString2x = date2x.toISOString().substr(11, 8);

    //document.getElementById("travel_time2x").innerHTML = 'Travel Time (at 10 m/s): ' + timeString2x + ' minutes';

    document.getElementById("precision").innerHTML = 'Mission precision: ~' + results['precision'].toFixed(2) + ' meters';
    //document.getElementById("precision2x").innerHTML = 'Mission precision: ~' + results['precision'].toFixed(2) + ' meters';
};