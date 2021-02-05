var slider = document.getElementById("gran_slider");
    var output = document.getElementById("gran_output");
    document.getElementById("gran_output").innerHTML = "Granularity: - meters"; // Display the default slider value

    // Update the current slider value (each time you drag the slider handle)

    var g_granu = 0
    var g_margin = 0
    slider.oninput = function() {
        g_granu = (g_distance/(this.value*50)).toFixed(2)
        document.getElementById("gran_output").innerHTML = "Granularity: "+ (g_distance/(this.value*50)).toFixed(2) + " meters";
        document.getElementById("margin_output").innerHTML = "Margin: " + (g_granu*g_margin).toFixed(2) + " meters";
        document.getElementById("margin_slider").style.visibility = "visible";
        document.getElementById("margin_output").style.visibility = "visible";
    }

    var slider = document.getElementById("margin_slider");
    var output = document.getElementById("margin_output");
    document.getElementById("margin_output").innerHTML = "Margin: - meters";

    // Update the current slider value (each time you drag the slider handle)
    slider.oninput = function() {
        g_margin = this.value;
        document.getElementById("margin_output").innerHTML = "Margin: " + (g_granu*this.value).toFixed(2) + " meters";
        document.getElementById("computeB").style.visibility = "visible";
    };